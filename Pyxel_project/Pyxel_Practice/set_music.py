import pyxel

pyxel.init(160, 120, title="音楽と効果音")

# 効果音の定義
pyxel.sounds[0].set(
    notes="C3E3G3C4",
    tones="T",
    volumes="7",
    effects="N",
    speed=20
)


def update():
    if pyxel.btnp(pyxel.KEY_SPACE):
        pyxel.play(0, 0)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.text(10, 10, "Press SPACE to play sound", 7)

pyxel.run(update, draw)

