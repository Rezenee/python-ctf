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
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load(os.path.join("images", "man.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.x_next = 0
        self.y_next = 0
        self.x_vel = 0
        self.y_vel = 0
        self.length = 25
        self.height = 50
        self.x_offset = (x_res / 2) - (self.length / 2) - self.rect.x
        self.y_offset = (y_res / 2) + (self.height / 2) + self.rect.y


    def move(self, direction):
        if 1 > self.x_vel > -1:
            if direction == "left":
                self.x_vel -= .2
            if direction == "right":
                self.x_vel += .2

    def movement(self):
        for i in walls:
            screen.blit(rainbow, (walls[i].rect.x + player1.x_offset, walls[i].rect.y + player1.y_offset),
                        (walls[i].rect.x + player1.x_offset, walls[i].rect.y + player1.y_offset, walls[i].l, walls[i].h))
        self.x_next = self.rect.x + self.x_vel * dt
        self.terrain_collision()
        self.rect.x += self.x_vel * dt
        # FRICTION
        if self.x_vel > 0:
            self.x_vel = self.x_vel - .05
        if self.x_vel < 0:
            self.x_vel = self.x_vel + .05
        if .05 > self.x_vel > -.05:
            self.x_vel = 0
        self.x_offset = (x_res / 2) - (self.length / 2) - self.rect.x
        self.y_offset = (y_res / 2) + (self.height / 2) - self.rect.y

    def terrain_collision(self):
        pass

player1 = player()


class block(pg.sprite.Sprite):
    def __init__(self, x, y, length, height, colour):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface([length, height])
        self.image.fill(colour)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.l = length
        self.h = height
        self.colour = colour


def update():
    screen.blit(player1.image, (center_x - player1.length / 2, center_y - player1.height / 2))
    # for i in walls:
    #     pg.draw.rect(screen, walls[i].colour, (walls[i].x + player1.x_offset, walls[i].y + player1.y_offset, walls[i].l, walls[i].h))
    for i in walls:
        screen.blit(walls[i].image, (walls[i].rect.x + player1.x_offset, walls[i].rect.y + player1.y_offset, walls[i].l, walls[i].h))
    pg.display.update()


def initial_draw():
    screen.blit(background, (0, 0))
    pg.display.update()


initial_draw()

walls = {
        'ground': block(0, 0, 100, 20, grey),
        'wall': block(-25, -50, 25, 25, grey)
         }


while 1:
    dt = clock.tick(0)

    keys = pg.key.get_pressed()
    print(clock.get_fps())
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

