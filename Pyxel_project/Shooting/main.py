import pyxel
import random

# --- 定数定義 ---
SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
PLAYER_U = 0
PLAYER_V = 0
ENEMY_U = 16
ENEMY_V = 0
BULLET_U = 32
BULLET_V = 0
SIZE = 16

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = 30
        self.color = random.choice([8, 10, 11])  # 赤、オレンジ、黄
        self.vx = random.uniform(-1.5, 1.5)
        self.vy = random.uniform(-1.5, 1.5)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.vx *= 0.95
        self.vy *= 0.95

    def draw(self):
        if self.life > 0:
            size = max(1, self.life // 10)
            pyxel.circ(self.x, self.y, size, self.color)

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_active = True

    def update(self):
        self.y -= 4
        if self.y < -SIZE:
            self.is_active = False

    def draw(self):
        if self.is_active:
            pyxel.blt(self.x, self.y, 0, BULLET_U, BULLET_V, SIZE, SIZE, 0)

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_active = True

    def update(self):
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.is_active = False

    def draw(self):
        if self.is_active:
            pyxel.blt(self.x, self.y, 0, ENEMY_U, ENEMY_V, SIZE, SIZE, 0)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Pyxel Shooter")

        try:
            pyxel.load("assets/my_shooter.pyxres")
        except FileNotFoundError:
            print("エラー: 'assets/my_shooter.pyxres'が見つかりません。")
            pyxel.quit()

        pyxel.sounds[0].set("c2e2g2c3", "T", "7654", "N", 10) #爆破音
        pyxel.sounds[1].set("a1f1", "T", "7777", "N", 20)  # 被弾音

        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲーム初期化"""
        self.player_x = SCREEN_WIDTH // 2 + SIZE // 2
        self.player_y = SCREEN_HEIGHT - 16
        self.bullets = []
        self.enemies = []
        self.particles = []
        self.enemy_spawn_timer = 0
        self.score = 0
        self.lives = 3
        self.game_over = False

    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()
            return

        self.update_player()
        self.update_enemies()
        self.update_bullets()
        self.update_particles()
        self.check_collisions()
        self.spawn_enemies()

        self.bullets = [b for b in self.bullets if b.is_active]
        self.enemies = [e for e in self.enemies if e.is_active]
        self.particles = [p for p in self.particles if p.life > 0]

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, SCREEN_WIDTH - SIZE)

        if pyxel.btnp(pyxel.KEY_SPACE):
            bullet = Bullet(self.player_x + SIZE // 2 - 2, self.player_y)
            self.bullets.append(bullet)

    def update_enemies(self):
        for enemy in self.enemies:
            enemy.update()
            # 敵がプレイヤーに到達したらライフ減少
            if enemy.y + SIZE >= self.player_y and abs(enemy.x - self.player_x) < SIZE:
                enemy.is_active = False
                pyxel.play(0, 1)  # 被弾音
                self.lives -= 1
                self.create_explosion(self.player_x + SIZE // 2, self.player_y)
                if self.lives <= 0:
                    self.game_over = True

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.update()

    def update_particles(self):
        for particle in self.particles:
            particle.update()

    def spawn_enemies(self):
        """スコアに応じて敵の出現間隔・速度を調整"""
        self.enemy_spawn_timer += 1

        # --- 難易度調整 ---
        # スコアが上がるほど敵が速く・多く出る
        spawn_rate = max(30 - self.score // 50, 5)  # 最小5フレーム間隔
        enemy_speed = 1 + self.score // 200          # スコア200ごとに速く

        if self.enemy_spawn_timer >= spawn_rate:
            x = random.randint(0, SCREEN_WIDTH - SIZE)
            self.enemies.append(Enemy(x, -SIZE, enemy_speed))
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
                if (bullet.x < enemy.x + SIZE and
                    bullet.x + 4 > enemy.x and
                    bullet.y < enemy.y + SIZE and
                    bullet.y + 8 > enemy.y):
                    bullet.is_active = False
                    enemy.is_active = False
                    pyxel.play(0, 0)
                    self.create_explosion(enemy.x + SIZE // 2, enemy.y + SIZE // 2)
                    self.score += 10

    def draw(self):
        pyxel.cls(0)
        for enemy in self.enemies:
            enemy.draw()
        for bullet in self.bullets:
            bullet.draw()
        for particle in self.particles:
            particle.draw()
        pyxel.blt(self.player_x, self.player_y, 0, PLAYER_U, PLAYER_V, SIZE, SIZE, 0)

        # スコアとライフ表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 7)
        pyxel.text(120, 5, f"LIVES: {self.lives}", 8)

        # ゲームオーバー画面
        if self.game_over:
            pyxel.cls(0)
            pyxel.text(50, 50, "GAME OVER", 8)
            pyxel.text(40, 70, f"FINAL SCORE: {self.score}", 7)
            pyxel.text(30, 90, "Press SPACE to Restart", 6)

App()
