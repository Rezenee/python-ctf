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
    def move(self, direction):
        if 1 > self.x_vel > -1:
            if direction == "left":
                self.x_vel -= .2
            if direction == "right":
                self.x_vel += .2

    def movement(self):
        for i in walls:
            screen.blit(rainbow, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset),
                        (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))
        self.x_next = self.x + self.x_vel * dt
        self.terrain_collision()
        self.x += self.x_vel * dt

        # FRICTION
        if self.x_vel > 0:
            self.x_vel = self.x_vel - .05
        if self.x_vel < 0:
            self.x_vel = self.x_vel + .05
        if .05 > self.x_vel > -.05:
            self.x_vel = 0
        self.x_offset = (x_res / 2) - (self.length / 2) - self.x
        self.y_offset = (y_res / 2) + (self.height / 2) - self.y

    def terrain_collision(self):
     # X COLLISION
        for wall in walls:
            print(self.y, 'self.y')
            print(walls[wall].y + walls[wall].h + self.height)
            # Moving into the right side of block
            if walls[wall].x + walls[wall].l > self.x_next > walls[wall].x and walls[wall].y + walls[wall].h + self.height > self.y > walls[wall].y:
                self.x_vel = 0
                self.x = walls[wall].x + walls[wall].l
            # Moving into left side of block
            if walls[wall].x < self.x_next + self.length < walls[wall].x + walls[wall].l and walls[wall].y + walls[wall].h + self.height > self.y > walls[wall].y:
                self.x_vel = 0
                self.x = walls[wall].x - self.length

player1 = player()


class block:
    def __init__(self, x, y, length, height, colour):
        self.x = x
        self.y = y
        self.l = length
        self.h = height
        self.colour = colour


def update():
    screen.blit(player1.image, (center_x - player1.length / 2, center_y - player1.height / 2))
    for i in walls:
        pg.draw.rect(screen, walls[i].colour, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))

    pg.display.update()


def initial_draw():
    screen.blit(background, (0, 0))
    pg.display.update()


initial_draw()

walls = {
        # 'ground': block(0, 0, 100, 20, grey),
        'wall': block(-25, -1, 25, 25, grey),
        'wall2': block(50, -74,25, 25, grey)
         }


while 1:
    dt = clock.tick(60)

    keys = pg.key.get_pressed()
    #print(clock.get_fps())
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

    if keys[pg.K_a] and keys[pg.K_d] != 1:
        player1.move("left")
    if keys[pg.K_d] and keys[pg.K_a] != 1:
        player1.move("right")

    player1.movement()
    update()
