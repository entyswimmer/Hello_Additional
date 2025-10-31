import pyxel

def update():
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.text(10, 50, "Hello Pyxel on Raspberry Pi!", 7)

pyxel.init(160, 120, title="Pyxel Test")
pyxel.run(update, draw)
