import pyxel

pyxel.init(160, 120, title="音楽システム")

# 音楽の定義
pyxel.sounds[0].set("C3", "T", "7", "N", 30)
pyxel.sounds[1].set("E3", "T", "7", "N", 30)
pyxel.sounds[2].set("G3", "T", "7", "N", 30)
pyxel.sounds[3].set("C3E3G3C4", "N", "7654", "NFNF", 10)

music_playing = False

def update():
    global music_playing

    if pyxel.btnp(pyxel.KEY_SPACE):
        if not music_playing:
            pyxel.playm(0, loop=True)
            music_playing = True
        else:
            pyxel.stop()
            music_playing = False

    if pyxel.btnp(pyxel.KEY_1):
        pyxel.play(0, 0)
    if pyxel.btnp(pyxel.KEY_2):
        pyxel.play(1, 1)
    if pyxel.btnp(pyxel.KEY_3):
        pyxel.play(2, 2)

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.text(10, 10, "Press SPACE to toggle music", 7)
    pyxel.text(10, 20, "Press 1, 2, 3 for sound effects", 7)
    pyxel.text(10, 30, "Music playing: " + str(music_playing), 8)

pyxel.musics[0].set([0], [1], [2], [3])
pyxel.run(update, draw)

