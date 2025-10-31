import pyxel
import math

pyxel.init(160, 120, title="衝突判定の改善")

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

def check_collision(circle, rect):
    closest_x = max(rect.x, min(circle.x, rect.x + rect.width))
    closest_y = max(rect.y, min(circle.y, rect.y + rect.height))

    distance = math.sqrt((circle.x - closest_x) ** 2 + (circle.y - closest_y) ** 2)

    return distance < circle.radius

circle = Circle(80, 60, 10)
rectangle = Rectangle(100, 50, 40, 20)

def update():
    circle.x = pyxel.mouse_x
    circle.y = pyxel.mouse_y

    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(0)
    pyxel.circ(circle.x, circle.y, circle.radius, 11)
    pyxel.rect(rectangle.x, rectangle.y, rectangle.width, rectangle.height, 8)

    if check_collision(circle, rectangle):
        pyxel.text(10, 10, "Collision Detected!", 7)

pyxel.run(update, draw)

