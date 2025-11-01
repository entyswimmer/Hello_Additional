import pyxel
import random

# 定数
SCENE_TITLE = 0
SCENE_GAME = 1
SCENE_RESULT = 2

# じゃんけんの手 (0: グー, 1: チョキ, 2: パー)
ROCK = 0
SCISSORS = 1
PAPER = 2
HANDS = [ROCK, SCISSORS, PAPER]
HAND_NAMES = ["ROCK", "SCISSORS", "PAPER"]

# ゲームの状態変数
class App:
    def __init__(self):
        # ウィンドウサイズ: 160x120
        pyxel.init(160, 120, title="じゃんけんゲーム")
        pyxel.mouse(True)  # マウスカーソルを表示

        self.scene = SCENE_TITLE
        self.player_hand = -1  # プレイヤーの手 (-1: 未選択)
        self.cpu_hand = -1     # CPUの手
        self.result_text = ""  # 結果テキスト

        # 効果音の設定 (サウンド番号 0: 勝ち, 1: あいこ, 2: 負け)
        pyxel.sounds[0].set(
            "C3E3G3C4",
            "S",
            "7777",
            "NSNF",
            6
        )

        pyxel.sounds[1].set(
            "C3",
            "S",
            "6",
            "N",
            5
        )

        pyxel.sounds[2].set(
            "C3E3G3C3",
            "S",
            "765",
            "FFF",
            8
        )

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.scene == SCENE_TITLE:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
                self.scene = SCENE_GAME
                self.reset_game()

        elif self.scene == SCENE_GAME:
            self.handle_mouse_input()

        elif self.scene == SCENE_RESULT:
            # 2秒後にタイトル画面に戻る (120フレーム)
            if pyxel.frame_count % 120 == 0:
                self.scene = SCENE_TITLE

    def handle_mouse_input(self):
        # マウス左クリックが押された瞬間
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y

            # グーの判定エリア (x: 20-50, y: 70-100)
            if 20 <= mx < 50 and 70 <= my < 100:
                self.player_hand = ROCK
            # チョキの判定エリア (x: 65-95, y: 70-100)
            elif 65 <= mx < 95 and 70 <= my < 100:
                self.player_hand = SCISSORS
            # パーの判定エリア (x: 110-140, y: 70-100)
            elif 110 <= mx < 140 and 70 <= my < 100:
                self.player_hand = PAPER

            # プレイヤーの手が確定したら結果判定へ
            if self.player_hand != -1:
                self.determine_result()

    def determine_result(self):
        self.cpu_hand = random.choice(HANDS) # CPUの手をランダムに決定
        # 結果判定
        # (プレイヤーの手 - CPUの手) の結果で判定
        # 0: あいこ, 1, -2: 勝ち, -1, 2: 負け
        diff = self.player_hand - self.cpu_hand

        if diff == 0:
            self.result_text = "Draw..."
            pyxel.play(3, 1) # チャンネル3でサウンド1(あいこ)を再生
        elif diff in [1, -2]:
            self.result_text = "You win!"
            pyxel.play(3, 0) # チャンネル3でサウンド0(勝ち)を再生
        else: # diff in [-1, 2]
            self.result_text = "You lose..."
            pyxel.play(3, 2) # チャンネル3でサウンド2(負け)を再生

        self.scene = SCENE_RESULT

    def reset_game(self):
        self.player_hand = -1
        self.cpu_hand = -1
        self.result_text = ""

    def draw(self):
        pyxel.cls(1) # 画面を黒でクリア (色番号0)

        if self.scene == SCENE_TITLE:
            pyxel.text(40, 40, "ROCK! SCISSORS! PAPER! 123!", 7) # 白 (色番号7)
            pyxel.text(30, 60, "Click or Press SPACE to Start", 3) # シアン (色番号3)

        elif self.scene == SCENE_GAME:
            pyxel.text(45, 10, "Choice your hand", 7)

            # CPUの手の場所 (ここではまだ表示しない)
            pyxel.text(70, 40, "CPU: ?", 7)

            # プレイヤーの手の選択肢 (テキスト表示とクリックエリア)
            self.draw_hand_choice(20, 70, HAND_NAMES[ROCK], ROCK)
            self.draw_hand_choice(65, 70, HAND_NAMES[SCISSORS], SCISSORS)
            self.draw_hand_choice(110, 70, HAND_NAMES[PAPER], PAPER)

        elif self.scene == SCENE_RESULT:
            # 結果表示
            pyxel.text(50, 10, "Result", 3)

            pyxel.text(10, 40, f"CPU: {HAND_NAMES[self.cpu_hand]}", 3)
            pyxel.text(10, 60, f"YOU: {HAND_NAMES[self.player_hand]}", 3)

            pyxel.text(60 - len(self.result_text)*2, 90, self.result_text, 8 if self.result_text == "You win!" else 6) # 黄色/ピンクで結果を強調
    
    def draw_hand_choice(self, x, y, name, hand_index):
        # クリックエリアの枠を描画 (30x30ピクセル)
        # マウスオーバーで色を変える
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        is_hover = x <= mx < x + 30 and y <= my < y + 30
        
        # 四角を描画 (x, y, 幅, 高さ, 色)
        color = 3 if is_hover else 5 # ホバー: シアン(3), 通常: マゼンタ(5)
        pyxel.rectb(x, y, 30, 30, color) 
        
        # 手の名前を枠内に表示
        pyxel.text(x + 5, y + 10, name, 7) # 白 (色番号7)

app = App()
pyxel.run(app.update, app.draw)
