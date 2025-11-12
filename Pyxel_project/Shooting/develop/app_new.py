import pyxel
import random
from objects import Particle, Star, Bullet, Enemy

# シーン定数
SCENE_TITLE = 0
SCENE_GAME = 1
SCENE_GAMEOVER = 2

# --- 仮想パッド (V-Pad) の定数 ---
# 画面サイズが160x120なので、画面下に配置する
PAD_Y = 100 
BUTTON_W = 20
BUTTON_H = 18
MARGIN = 5

class App:
    def __init__(self, constants):
        self.C = constants

        # 幅160, 高さ120で初期化。タッチ操作に備え、画面外にカーソルを表示
        pyxel.init(self.C["SCREEN_WIDTH"], self.C["SCREEN_HEIGHT"], title="Pyxel Shooter")
        pyxel.mouse(True) # マウスカーソルを常に表示 (タッチ操作用)

        try:
            pyxel.load("assets/my_shooter.pyxres")
        except FileNotFoundError:
            print("エラー: 'assets/my_shooter.pyxres'が見つかりません。")
            pyxel.quit()

        # サウンド設定
        pyxel.sounds[0].set("c2e2g2c3", "T", "7654", "N", 10) # 爆破音
        pyxel.sounds[1].set("a1f1", "T", "7777", "N", 20)  # 被弾音
        
        self.scene = SCENE_TITLE
        self.score = 0
        self.lives = 3
        
        # V-Padの状態を保持する変数 (タッチ入力時にTrue/Falseを切り替える)
        self.is_left_pressed = False
        self.is_right_pressed = False
        self.is_shoot_pressed = False

        self.reset_game()
        
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲーム初期化 (ゲーム開始時またはリスタート時に呼ばれる)"""
        self.player_x = self.C["SCREEN_WIDTH"] // 2 + self.C["SIZE"] // 2
        self.player_y = self.C["SCREEN_HEIGHT"] - 16
        self.bullets = []
        self.enemies = []
        self.particles = []
        self.stars = [Star() for _ in range(100)]
        self.enemy_spawn_timer = 0
        self.lives = 3
        
    # --- タッチ操作判定ヘルパー ---
    def is_touching_area(self, x, y, w, h):
        """指定領域がタッチされているか判定する"""
        # pyxel.btnv(pyxel.MOUSE_BUTTON_LEFT) はタッチ操作を検出
        if pyxel.btnv(pyxel.MOUSE_BUTTON_LEFT):
            mx = pyxel.mouse_x
            my = pyxel.mouse_y
            # マウスポジションが領域内にあるか
            return x <= mx < x + w and y <= my < y + h
        return False

    # --- メインロジック ---
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # V-Padの状態をリセットし、タッチ入力をチェック
        self.check_vpad_input()

        if self.scene == SCENE_TITLE:
            self.update_title()
        elif self.scene == SCENE_GAME:
            self.update_game()
        elif self.scene == SCENE_GAMEOVER:
            self.update_gameover()

    def check_vpad_input(self):
        """仮想パッドのタッチ入力を検出し、状態変数に保存する"""
        
        # 左ボタンの領域: (MARGIN, PAD_Y, BUTTON_W, BUTTON_H)
        self.is_left_pressed = self.is_touching_area(MARGIN, PAD_Y, BUTTON_W, BUTTON_H)
        
        # 右ボタンの領域: (MARGIN + BUTTON_W + MARGIN, PAD_Y, BUTTON_W, BUTTON_H)
        right_x = MARGIN + BUTTON_W + MARGIN
        self.is_right_pressed = self.is_touching_area(right_x, PAD_Y, BUTTON_W, BUTTON_H)
        
        # ショットボタンの領域: (画面右端付近)
        shoot_x = self.C["SCREEN_WIDTH"] - BUTTON_W - MARGIN
        self.is_shoot_pressed = self.is_touching_area(shoot_x, PAD_Y, BUTTON_W, BUTTON_H)
        

    # --- シーンごとのアップデート ---
    # update_title, update_game, update_gameover, update_enemies, update_bullets, update_particles, 
    # spawn_enemies, create_explosion, check_collisions はロジック変更なし（省略）
    def update_title(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or self.is_shoot_pressed: # タッチも追加
            self.scene = SCENE_GAME
            self.score = 0
            self.reset_game()

    def update_game(self):
        """ゲーム中の更新ロジック"""
        self.update_player()
        self.update_enemies()
        self.update_bullets()
        self.update_particles()
        self.update_stars()
        self.check_collisions()
        self.spawn_enemies()

        self.bullets = [b for b in self.bullets if b.is_active]
        self.enemies = [e for e in self.enemies if e.is_active]
        self.particles = [p for p in self.particles if p.life > 0]
        
        if self.lives <= 0:
            self.scene = SCENE_GAMEOVER

    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_SPACE) or self.is_shoot_pressed: # タッチも追加
            self.scene = SCENE_TITLE
            
    # --- 既存のゲームアップデートロジック ---
    def update_player(self):
        # キーボード入力 (A, D, 矢印) または V-Padの入力で移動
        move_left = pyxel.btn(pyxel.KEY_A) or pyxel.btn(pyxel.KEY_LEFT) or self.is_left_pressed
        move_right = pyxel.btn(pyxel.KEY_D) or pyxel.btn(pyxel.KEY_RIGHT) or self.is_right_pressed

        if move_left:
            self.player_x = max(self.player_x - 2, 0)
        if move_right:
            self.player_x = min(self.player_x + 2, self.C["SCREEN_WIDTH"] - self.C["SIZE"])

        # スペースキーまたはV-Padのショットボタンで発射
        if pyxel.btnp(pyxel.KEY_SPACE) or (self.scene == SCENE_GAME and self.is_shoot_pressed and pyxel.btnr(pyxel.MOUSE_BUTTON_LEFT)):
            # btnr() (ボタンを離した瞬間) を使うことで、押しっぱなしでの連射を防ぐ
            bullet = Bullet(self.player_x + self.C["SIZE"] // 2 - 2, self.player_y, self.C)
            self.bullets.append(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()
            if enemy.y + self.C["SIZE"] >= self.player_y and abs(enemy.x - self.player_x) < self.C["SIZE"]:
                enemy.is_active = False
                pyxel.play(0, 1)
                self.lives -= 1
                self.create_explosion(self.player_x + self.C["SIZE"] // 2, self.player_y)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def update_particles(self):
        for particle in self.particles:
            particle.update()
    
    def update_stars(self):
        for star in self.stars:
            star.update()

    def spawn_enemies(self):
        self.enemy_spawn_timer += 1
        spawn_rate = max(30 - self.score // 50, 5)
        enemy_speed = 1 + self.score // 200

        if self.enemy_spawn_timer >= spawn_rate:
            x = random.randint(0, self.C["SCREEN_WIDTH"] - self.C["SIZE"])
            self.enemies.append(Enemy(x, -self.C["SIZE"], enemy_speed, self.C))
            self.enemy_spawn_timer = 0

    def create_explosion(self, x, y):
        for _ in range(10):
            self.particles.append(Particle(x, y))

    def check_collisions(self):
        for bullet in self.bullets:
            if not bullet.is_active:
                continue
            for enemy in self.enemies:
                if not enemy.is_active:
                    continue
                
                if (bullet.x < enemy.x + self.C["SIZE"] and
                    bullet.x + 4 > enemy.x and
                    bullet.y < enemy.y + self.C["SIZE"] and
                    bullet.y + 8 > enemy.y):

                    bullet.is_active = False
                    enemy.is_active = False
                    pyxel.play(0, 0)
                    self.create_explosion(enemy.x + self.C["SIZE"] // 2, enemy.y + self.C["SIZE"] // 2)
                    self.score += 10

    # --- 描画ロジック ---
    def draw(self):
        pyxel.cls(0)

        if self.scene == SCENE_TITLE:
            self.draw_title()
        elif self.scene == SCENE_GAME:
            self.draw_game()
        elif self.scene == SCENE_GAMEOVER:
            self.draw_gameover()

        # ゲーム中またはタイトル画面で、V-Padを描画
        if self.scene in (SCENE_TITLE, SCENE_GAME):
            self.draw_vpad()

    def draw_title(self):
        screen_center_x = self.C["SCREEN_WIDTH"] // 2
        title_text = "PYXEL SHOOTER"
        pyxel.text(screen_center_x - len(title_text) * 2, 40, title_text, 8) 
        pyxel.blt(screen_center_x - self.C["SIZE"] // 2, 60, 0, self.C["PLAYER_U"], self.C["PLAYER_V"], self.C["SIZE"], self.C["SIZE"], 0)
        
        guide_text = "USE V-PAD (TOUCH) TO START/MOVE"
        if pyxel.frame_count % 30 < 15:
            pyxel.text(screen_center_x - len(guide_text) * 2, 90, guide_text, 7)

    def draw_game(self):
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for particle in self.particles:
            particle.draw()
        for star in self.stars:
            star.draw()
            
        pyxel.blt(self.player_x, self.player_y, 0, self.C["PLAYER_U"], self.C["PLAYER_V"], self.C["SIZE"], self.C["SIZE"], 0)

        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(120, 5, f"LIVES: {self.lives}", 8)
        
    def draw_gameover(self):
        screen_center_x = self.C["SCREEN_WIDTH"] // 2
        
        pyxel.text(screen_center_x - len("GAME OVER") * 2, 50, "GAME OVER", 8)
        
        score_text = f"FINAL SCORE: {self.score}"
        pyxel.text(screen_center_x - len(score_text) * 2, 70, score_text, 7)
        
        restart_text = "Press TOUCH for Title"
        pyxel.text(screen_center_x - len(restart_text) * 2, 90, restart_text, 6)
        
    def draw_vpad(self):
        """仮想パッドの描画ロジック"""
        
        # --- 左ボタン ---
        color_left = 3 if self.is_left_pressed else 13 # 押されていたら暗い色、そうでなければ明るい色
        pyxel.rect(MARGIN, PAD_Y, BUTTON_W, BUTTON_H, color_left)
        pyxel.text(MARGIN + 6, PAD_Y + 5, "<", 0) # 記号
        
        # --- 右ボタン ---
        right_x = MARGIN + BUTTON_W + MARGIN
        color_right = 3 if self.is_right_pressed else 13
        pyxel.rect(right_x, PAD_Y, BUTTON_W, BUTTON_H, color_right)
        pyxel.text(right_x + 6, PAD_Y + 5, ">", 0)
        
        # --- ショットボタン ---
        shoot_x = self.C["SCREEN_WIDTH"] - BUTTON_W - MARGIN
        color_shoot = 8 if self.is_shoot_pressed else 10 # 押されていたら赤、そうでなければオレンジ
        pyxel.rect(shoot_x, PAD_Y, BUTTON_W, BUTTON_H, color_shoot)
        pyxel.text(shoot_x + 3, PAD_Y + 5, "SHOT", 0)