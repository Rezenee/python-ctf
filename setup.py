import pygame as pg
import time
import os
res = x_res, y_res = 1920, 1080
center_x = x_res / 2
center_y = y_res / 2
pg.init()
screen = pg.display.set_mode(res)
fullscreen_check = 0
# SPRITES
background = pg.image.load(os.path.join("images", "wallpaper.jpg")).convert()
background = pg.transform.scale(background, (x_res, y_res))
player_sprite = pg.image.load(os.path.join("images", "man.png")).convert_alpha()


clock = pg.time.Clock()
blue = (0, 0, 255)
black = (0, 0, 0)
white = (200,200,200)
grey = (125, 125, 125)
green = (37, 115, 58)
red = (255, 0, 0)

class player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_vel = 0
        self.y_vel = 0
        self.length = 25
        self.height = 50
        self.x_offset = (x_res / 2) - (self.length / 2) - self.x
        self.y_offset = (y_res / 2) + (self.height / 2) + self.y

    def move(self, direction):
        self.x_offset = (x_res / 2) - (self.length / 2) - self.x
        self.y_offset = (y_res / 2) + (self.height / 2) - self.y

        if 10 > self.x_vel > -10:
            if direction == "left":
                self.x_vel -= 1
            if direction == "right":
                self.x_vel += 1

    def movement(self):
        self.x += self.x_vel

        # FRICTION

        if self.x_vel > 0:
            self.x_vel -= .1
        if self.x_vel < 0:
            self.x_vel += .1
        else:
            self.x_vel = 0


player1 = player()


class block:
    def __init__(self, x, y, length, height, colour):
        self.x = x
        self.y = y
        self.l = length
        self.h = height
        self.colour = colour


def update():
    screen.blit(background, (0, 0))

    screen.blit(player_sprite, (center_x - player1.length / 2, center_y - player1.height / 2))
    for i in walls:
        pg.draw.rect(screen, walls[i].colour, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))
    pg.display.update()


def initial_draw():
    screen.blit(background, (0, 0))
    pg.display.update()


initial_draw()

walls = {'ground': block(0, 0, 100, 20, grey)
         }


while 1:
    dt = clock.tick(60)

    keys = pg.key.get_pressed()
    print(player1.x_vel, "x_vel")
    print(player1.x, "x")
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
    if keys[pg.K_d]:
        player1.move("right")
    if keys[pg.K_a]:
        player1.move("left")
    player1.movement()
    update()

