import pygame as pg
import time
import os
res = x_res, y_res = 1024, 768
center_x = x_res / 2
center_y = y_res / 2
pg.init()
screen = pg.display.set_mode(res)
fullscreen_check = 0
# SPRITES
background = pg.image.load(os.path.join("images", "wallpaper.jpg")).convert()
background = pg.transform.scale(background, (x_res, y_res))
rainbow = pg.image.load(os.path.join("images", "rainbow-fade.jpg")).convert()
rainbow = pg.transform.scale(rainbow, (x_res,y_res))
clock = pg.time.Clock()
blue = (0, 0, 255)
black = (0, 0, 0)
white = (200,200,200)
grey = (125, 125, 125)
green = (37, 115, 58)
red = (255, 0, 0)

chunk_size = 640
blockPlaced = 0
class player(pg.sprite.Sprite):
    def __init__(self):
        self.image = pg.image.load(os.path.join("images", "man.png")).convert_alpha()
        self.x = 0
        self.y = 0
        self.x_next = 0
        self.y_next = 0
        self.x_vel = 0
        self.y_vel = 0
        self.length = 25
        self.height = 50
        self.x_offset = (x_res / 2) - (self.length / 2) - self.x
        self.y_offset = (y_res / 2) + (self.height / 2) + self.y
        self.grounded = 0
        self.ground_counter = 0
        self.x_chunk, self.y_chunk = self.coordinate = (self.x // chunk_size, self.y // chunk_size)

    def move(self, direction):
        x_accel = .3

        if direction == "left":
            self.x_vel = -x_accel
        if direction == "right":
            self.x_vel = x_accel
        if direction == "up":
            if self.grounded:
                self.y_vel -= 1.8
                self.grounded = 0
    def movement(self):
        # for i in walls:
        #   (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))
        for chunk in walls:
            if self.x_chunk + 1 >= int(chunk) >= self.x_chunk -1:
                for i in walls[chunk]:
                    screen.blit(background, (walls[chunk][i].x + self.x_offset, walls[chunk][i].y + self.y_offset),
                                (walls[chunk][i].x + self.x_offset, walls[chunk][i].y + self.y_offset, walls[chunk][i].l, walls[chunk][i].h))

        # Calculates the next position of X and Y coords
        self.x_next = self.x + self.x_vel * dt
        self.y_next = self.y + self.y_vel * dt

        # Runs collision detection-- Checks if you would run through blocks before applying change in coords
        self.terrain_collision()
        self.x_chunk, self.y_chunk = self.coordinate = (self.x // chunk_size, self.y // chunk_size)

        self.x += self.x_vel * dt
        self.y += self.y_vel * dt

        friction = .01
        # FRICTION
        if self.x_vel > 0:
            self.x_vel = self.x_vel - friction * dt
        if self.x_vel < 0:
            self.x_vel = self.x_vel + friction * dt
        if friction * dt > self.x_vel > -friction * dt:
            self.x_vel = 0

        # Gravity default = .015
        gravity = .015
        if self.y_vel < gravity * 30:
            self.y_vel += gravity * dt
            self.ground_counter += 1
            if self.ground_counter > 2:
                self.ground_counter = 0
                self.grounded = 0
        self.x_offset = (x_res / 2) - (self.length / 2) - self.x
        self.y_offset = (y_res / 2) + (self.height / 2) - self.y

    def terrain_collision(self):
        for chunk in walls:
            if self.x_chunk + 1 >= int(chunk) >= self.x_chunk - 1:
                for i in walls[chunk]:
                    # X COLLISION
                    #
                    # Checks for Y
                    if walls[chunk][i].y + walls[chunk][i].h + self.height > self.y > walls[chunk][i].y:
                        # Moving in the right direction
                        if self.x_vel > 0 and self.x < walls[chunk][i].x and self.x_next + self.length > walls[chunk][i].x:
                            self.x_vel = 0
                            self.x = walls[chunk][i].x - self.length
                        # Moving in the Left Direction
                        if self.x_vel < 0 and self.x >= walls[chunk][i].x + walls[chunk][i].l and self.x_next < walls[chunk][i].x + walls[chunk][i].l:
                            self.x_vel = 0
                            self.x = walls[chunk][i].x + walls[chunk][i].l
                    # Y COLLISION
                    #
                    # Checks for X
                    if walls[chunk][i].x - self.length < self.x < walls[chunk][i].x + walls[chunk][i].l:
                        # Falling Down Stops if hits block
                        if self.y_vel > 0 and self.y <= walls[chunk][i].y and self.y_next > walls[chunk][i].y:
                            self.y_vel = 0
                            self.y = walls[chunk][i].y
                            self.grounded = 1
                            self.ground_counter = 0
                        # Jumping stops if hits block
                        if self.y_vel < 0 and self.y - self.height > walls[chunk][i].y + walls[chunk][i].h and self.y_next - self.height < walls[chunk][i].y + walls[chunk][i].h:
                            self.y_vel = 0
                            self.y = walls[chunk][i].y + walls[chunk][i].h + self.height


    def place_block(self):
        if event.type == pg.MOUSEBUTTONDOWN:
            global blockPlaced
            mouse_x, mouse_y = mouse_pos = pg.mouse.get_pos()
            #screen.blit(player1.image, (center_x - player1.length / 2, center_y - player1.height / 2))
            # This makes the mouse be in the center of block when clicked, not the top right
            mouse_x -= 12
            mouse_y -= 12
            # if mouse_x - 12 >

            # This accounts for moving; 0,0 is center of screen not the top right
            mouse_x -= self.x_offset
            mouse_y -= self.y_offset



            mouse_x = int(mouse_x)
            mouse_y = int(mouse_y)
            chunk = mouse_x // chunk_size
            # Check to see if the chunk is already created
            varname = "playerBlock"
            varname += str(blockPlaced)
            blockPlaced += 1
            try:
                #     x, y, l, h, colour

                if walls[str(chunk)]:
                    walls[str(chunk)][varname] = block(mouse_x, mouse_y, 25, 25, blue)
            # If it has not been created
            except KeyError:
                walls[str(chunk)] = {}
                walls[str(chunk)][varname] = block(mouse_x, mouse_y, 25, 25, blue)


player1 = player()

class block:
    def __init__(self, x, y, length, height, colour):
        self.x = x
        self.y = y
        self.l = length
        self.h = height
        self.colour = colour
        self.x_cord = self.x // chunk_size
        self.y_cord = self.y // chunk_size

def update():
    screen.blit(player1.image, (center_x - player1.length / 2, center_y - player1.height / 2))
    for chunk in walls:
        if player1.x_chunk + 1 >= int(chunk) >= player1.x_chunk - 1:
            for i in walls[chunk]:
                pg.draw.rect(screen, walls[chunk][i].colour,(walls[chunk][i].x + player1.x_offset, walls[chunk][i].y + player1.y_offset, walls[chunk][i].l, walls[chunk][i].h))

    pg.display.update()

def initial_draw():
    screen.blit(background, (0, 0))
    pg.display.update()


initial_draw()
#     x, y, l, h, colour

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
    x = walls[wall].x
    chunk = x // chunk_size
    # Check to see if the chunk is already created
    try:
        if walls[str(chunk)]:
            walls[str(chunk)][str(wall)] = walls[wall]
    # If it has not been created
    except KeyError:
        walls[str(chunk)] = {}
        walls[str(chunk)][str(wall)] = walls[wall]
    del walls[wall]


### RUN LOOP
while 1:
    dt = clock.tick(0)
    keys = pg.key.get_pressed()
    #print(clock.get_fps())
    for event in pg.event.get():
        player1.place_block()
        if event.type == pg.QUIT:
            pg.quit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_F10:
                if fullscreen_check:
                    pg.display.set_mode(res)
                    fullscreen_check = 0
                else:
                    pg.display.set_mode(res, pg.FULLSCREEN)
                    fullscreen_check = 1
                initial_draw()
            if event.key == pg.K_SPACE:
                player1.move("up")
            if event.key == pg.K_ESCAPE:
                aoeuaoeu

    if keys[pg.K_a] and keys[pg.K_d] != 1:
        player1.move("left")
    if keys[pg.K_d] and keys[pg.K_a] != 1:
        player1.move("right")

    player1.movement()
    update()
