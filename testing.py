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
for wall in list(walls):
    x = walls[wall].x
    chunk_wall = 0
    distance = walls[wall].l
    end_point = x + distance
    increment = 0
    y = walls[wall].y
    h = walls[wall].h
    colour = walls[wall].colour
    if x + distance > chunk_size:
        if x < 0:
            while chunk_wall > x + chunk_size:
                chunk_wall -= chunk_size
            distance = abs(x) - abs(chunk_wall)
            walls[wall + str(increment)] = block(x, y, distance, h, colour)
            increment += 1
        else:
            while chunk_wall < x:
                chunk_wall += chunk_size
            distance = abs(chunk_wall) - abs(x)
            walls[wall + str(increment)] = block(x, y, distance, h, colour)
            increment += 1
        x = chunk_wall
        chunk_wall = 0
        while x < end_point:
            distance = chunk_size
            if x + chunk_size > end_point:
                distance = end_point - x
                walls[wall + str(increment)] = block(x, y, distance, h, colour)
                increment += 1
                break
            else:
                walls[wall + str(increment)] = block(x, y, distance, h, colour)
                increment += 1
            x += chunk_size
        del walls[wall]

for wall in list(walls):
    chunk = x // chunk_size
    if x < 0:
        chunk -= 1
    try:
        if walls[str(chunk)]:
            walls[str(chunk)][wall] = walls[wall]
    except KeyError:
        walls[str(chunk)] = {str(wall) : walls[wall]}
    del walls[wall]

