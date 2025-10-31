import pyxel

pyxel.init(160, 120, title="キー入力")

x = 80
y = 60

def update():
    global x, y

    if pyxel.btn(pyxel.KEY_LEFT):
        x = max(x - 2, 0)
    if pyxel.btn(pyxel.KEY_RIGHT):
        x = min(x + 2, 160)
    if pyxel.btn(pyxel.KEY_UP):
        y = max(y - 2, 0)
    if pyxel.btn(pyxel.KEY_DOWN):
        y = min(y + 2, 120)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.rect(x, y, 10, 10, 11)

pyxel.run(update, draw)

