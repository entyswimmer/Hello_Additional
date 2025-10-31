import pyxel

pyxel.init(160, 120, title="テキスト表示")

score = 0

def update():
    global score

    if pyxel.btnp(pyxel.KEY_SPACE):
        score += 10

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.text(10, 10, f"Score: {score}", 7)
    pyxel.text(10, 30, "Press SPACE to increase score", 6)
    pyxel.text(10, 50, "Press Q to quit", 8)

pyxel.run(update, draw)

