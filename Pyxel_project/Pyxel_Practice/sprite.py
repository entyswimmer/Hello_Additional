import pyxel

pyxel.init(160, 120, title="スプライト")

# スプライトの作成
pyxel.load("assets/my_asset.pyxres")

player_x = 80
player_y = 60

def update():
    global player_x, player_y
    
    if pyxel.btn(pyxel.KEY_LEFT):
        player_x = max(player_x - 2, 0)
    if pyxel.btn(pyxel.KEY_RIGHT):
        player_x = min(player_x + 2, 152)
    
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.blt(player_x, player_y, 0, 0, 0, 16, 16, 0)

pyxel.run(update, draw)
