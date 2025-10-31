import pyxel, random

particles = []

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-2, 0)
        self.life = 30

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1   # 重力
        self.life -= 1

    def draw(self):
        pyxel.pset(int(self.x), int(self.y), 10)

def update():
    if pyxel.btn(pyxel.KEY_SPACE):
        for _ in range(10):
            particles.append(Particle(80, 60))
    for p in particles[:]:
        p.update()
        if p.life <= 0:
            particles.remove(p)

def draw():
    pyxel.cls(0)
    for p in particles:
        p.draw()
    pyxel.text(5, 5, "Press SPACE to emit particles", 7)

pyxel.init(160, 120)
pyxel.run(update, draw)
