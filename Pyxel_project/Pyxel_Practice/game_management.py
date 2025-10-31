import pyxel
import random

pyxel.init(160, 120, title="ゲーム最適化")

class Star:
    def __init__(self):
        self.x = random.randint(0, 159)
        self.y = random.randint(0, 119)
        self.speed = random.uniform(0.5, 2)

    def update(self):
        self.y += self.speed
        if self.y > 120:
            self.y = 0
            self.x = random.randint(0, 159)

stars = [Star() for _ in range(100)]

def update():
    for star in stars:
        star.update()

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    for star in stars:
        pyxel.pset(int(star.x), int(star.y), 7)

    pyxel.text(5, 5, f"Stars: {len(stars)}", 8)
    pyxel.text(5, 15, f"FPS: {pyxel.frame_count}", 8)

pyxel.run(update, draw)

