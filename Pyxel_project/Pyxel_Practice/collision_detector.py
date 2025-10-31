import pyxel

pyxel.init(160, 120, title="コリジョン検出")

player_x = 80
player_y = 100
enemy_x = 80
enemy_y = 20

def update():
    global player_x, player_y, enemy_x, enemy_y

    if pyxel.btn(pyxel.KEY_LEFT):
        player_x = max(player_x - 2, 0)
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x = min(player_x + 2, 152)
    if pyxel.btn(pyxel.KEY_DOWN):
        player_y = min(player_y + 2, 112)
    if pyxel.btn(pyxel.KEY_UP):
        player_y = max(player_y - 2, 0)

    # 衝突判定
    if (abs(player_x - enemy_x) < 8 and abs(player_y - enemy_y) < 8):
        pyxel.play(0, 0)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.rect(player_x, player_y, 8, 8, 11)
    pyxel.rect(enemy_x, enemy_y, 8, 8, 8)

pyxel.sounds[0].set(notes="C3", tones="N", volumes="7", effects="N", speed=3)

pyxel.run(update, draw)

