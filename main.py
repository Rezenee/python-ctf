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
        self.coordinate = (self.x // chunk_size, self.y // chunk_size)
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
        global blit_dict
        for i in walls:
            screen.blit(background, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset),
                        (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))
        # Calculates the next position of X and Y coords
        self.x_next = self.x + self.x_vel * dt
        self.y_next = self.y + self.y_vel * dt

        # Runs collision detection-- Checks if you would run through blocks before applying change in coords
        self.terrain_collision()
        old_cord = self.coordinate       
        self.x_cord, self.y_cord = self.coordinate = (self.x // chunk_size, self.y // chunk_size)

        blit_dict = {k: v for k, v in walls.items() if self.x_cord + 1 >= walls[k].x_cord >= self.x_cord - 1 and self.y_cord + 1 >= walls[k].y_cord >= self.y_cord - 1} 
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

        # Gravity
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
        # X COLLISION
        #print(self.x_vel)
        for wall in walls:
            # X COLLISION
            #
            # Checks for Y
            if walls[wall].y + walls[wall].h + self.height > self.y > walls[wall].y:
                # Moving in the right direction
                if self.x_vel > 0 and self.x < walls[wall].x and self.x_next + self.length > walls[wall].x:
                    self.x_vel = 0
                    self.x = walls[wall].x - self.length
                # Moving in the Left Direction
                if self.x_vel < 0 and self.x >= walls[wall].x + walls[wall].l and self.x_next < walls[wall].x + walls[wall].l:
                    self.x_vel = 0
                    self.x = walls[wall].x + walls[wall].l
            # Y COLLISION
            #
            # Checks for X
            if walls[wall].x - self.length < self.x < walls[wall].x + walls[wall].l:
                # Falling Down Stops if hits block
                if self.y_vel > 0 and self.y <= walls[wall].y and self.y_next > walls[wall].y:
                    self.y_vel = 0
                    self.y = walls[wall].y
                    self.grounded = 1
                    self.ground_counter = 0
                # Jumping stops if hits block
                if self.y_vel < 0 and self.y - self.height > walls[wall].y + walls[wall].h and self.y_next - self.height < walls[wall].y + walls[wall].h:
                    self.y_vel = 0
                    self.y = walls[wall].y + walls[wall].h + self.height


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
    for i in walls:
        pg.draw.rect(screen, walls[i].colour, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))

    pg.display.update()


def initial_draw():
    screen.blit(background, (0, 0))
    pg.display.update()


initial_draw()
#     x, y, length, height, colour

walls = {
        'ground': block(-5000, 0, 10000, 20, grey),
        'wall': block(-25, -100, 25, 25, grey),
        'wall2': block(50, -45, 5, 25, grey)
        }
for wall in walls:
    x_checkChunk = walls[wall].x
    if x_checkChunk > 0:
        # Sees how close it is to the edge of chunk, then sees if with the length it goes into 2 chunks.
        while x_checkChunk > chunk_size:
           x_checkChunk -= chunk_size 
        if x_checkChunk + walls[wall].l> 640:
            
            del walls[wall]
    else:
        while x_checkChunk < -chunk_size:
            x_checkChunk += chunk_size
            print(x_checkChunk)
        if x_checkChunk - walls[wall].l< -chunk_size:
            print("oh god")
#print(walls)

while 1:
    dt = clock.tick(0)

    keys = pg.key.get_pressed()
   # print(clock.get_fps())
    for event in pg.event.get():
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
    if keys[pg.K_e] and keys[pg.K_a] != 1:
        player1.move("right")

    player1.movement()
    print(blit_dict) 
    update()
