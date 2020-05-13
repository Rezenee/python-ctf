grey = (200, 200, 200)
chunk_size = 640

class block:
    def __init__(self, x, y, length, height, colour):
        self.x = x
        self.y = y
        self.l = length
        self.h = height
        self.colour = colour
        self.x_cord = self.x // chunk_size
        self.y_cord = self.y // chunk_size

walls = {
        'ground': block(-5000, 0, 10000, 20, grey),
        'wall': block(-25, -100, 25, 25, grey),
        'wall2': block(1, -45, 25, 25, grey)
        }

walls[{'dictionary'}] = "'wall2': block(1, -45, 25, 25, grey)"

print(walls)