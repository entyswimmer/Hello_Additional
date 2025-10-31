import pyxel

pyxel.init(160, 120, title="図形描画")

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)

    # 線を描画
    pyxel.line(10, 10, 60, 60, 7)

    # 矩形を描画
    pyxel.rect(70, 10, 40, 40, 8)

    # 円を描画
    pyxel.circ(40, 80, 20, 12)

pyxel.run(update, draw)

