import pygame.draw
from spritesheet_functions import *
import constants


class ProjectileLog(object):

    def __init__(self):
        self.projectileLog = []


    def new_projectile(self, img, direction, x, y):
        if (len(self.projectileLog) < 10):
            self.projectileLog.append(Projectile(img, direction, x, y))

    def update(self, win):
        for p in self.projectileLog:
            p.update(win)
            if p.done:
                self.projectileLog.pop(self.projectileLog.index(p))

class Projectile(object):
    def __init__(self, type, direction, x, y):
        self.direction = direction
        self.curve = -3  # used to calculate projectile drop
        self.x = x
        self.y = y
        self.hitBox = pygame.Rect(x, y, 10, 10)
        self.animationCounter = 0   # to rotate projectile. for animation
        self.type = type  # refers to weapon type. none, boxing glove, etc
        self.damage = 0  # how much knockback it creates

        if type == "BOXING_GLOVE":
            self.img = SpriteSheet(constants.SS_BOXING_GLOVE)
            self.damage = constants.BOXING_GLOVE_DMG
        elif type == "FIREBALL":
            self.img = SpriteSheet(constants.SS_FIREBALL)
            self.damage = constants.FIREBALL_DMG
        else:
            self.img = SpriteSheet(constants.IMG_NINJA_STAR)
            self.damage = constants.BASIC_ATTACK_DMG

        # True after bullet hits an enemy or bullet goes beyond screen
        self.done = False

    def update(self, win):
        self.animationCounter += 1
        if self.type == "BOXING_GLOVE":
            self.use_boxing_glove(win)
        elif self.type == "FIREBALL":
            self.use_fireball(win)
        else:
            self.use_default_attack(win)


    def use_default_attack(self, win):
        self.x += constants.PROJECTILE_SPEED * self.direction
        self.y += self.curve
        self.curve += .5

        if (self.x > constants.WINDOW_WIDTH - 100) or (
                self.x < 100) or self.y > constants.WINDOW_HEIGHT - 50 or self.y < 10:
            self.done = True;

        else:
            self.hitBox = pygame.Rect(self.x, self.y, 10, 10)

        frame = pygame.transform.scale2x(self.img.get_image(0, 0, 16, 16))

        if self.animationCounter % 2 == 0:
            frame = pygame.transform.rotate(frame, 45)

        win.blit(frame, (self.x - 8, self.y - 8))
        # pygame.draw.circle(win, (60,60,60), self.cRect.center, 10)

    def use_boxing_glove(self, win):
        buffer = 10 # pixels punch is away from character
        if self.animationCounter >= 6:
            self.done = True
        else:
            axis = self.animationCounter * 8

            if self.direction == 1:
                self.hitBox = pygame.Rect(self.x + 32 + buffer, self.y, int(32 / 6 * self.animationCounter), 64)
                frame = pygame.transform.scale((self.img.get_image(axis, 0, 8, 16)), (32, 64))
            else:
                self.hitBox = pygame.Rect(self.x - int(32 / 6 * self.animationCounter) - buffer, self.y, int(32 / 6 * self.animationCounter), 64)
                frame = pygame.transform.scale((self.img.get_image(axis, 0, 8, 16)), (32, 64))
                frame = pygame.transform.flip(frame, True, False)

            win.blit(frame, (self.x +((32 + buffer) * self.direction), self.y))

            # for hitbox debugging
            #pygame.draw.rect(win, (60,60,60), self.hitBox, 1)

    def use_fireball(self, win):
        self.x += constants.FIREBALL_SPEED * self.direction

        if self.x > constants.WINDOW_WIDTH - 100 or self.x < 100:
            self.done = True;

        else:
            if self.animationCounter >= 8:
                self.animationCounter = 7

            axis = self.animationCounter // 2 * 16

            if self.direction == 1:
                frame = pygame.transform.scale((self.img.get_image(axis, 0, 16, 16)), (32, 32))
            else:
                frame = pygame.transform.scale((self.img.get_image(axis, 0, 16, 16)), (32, 32))
                frame = pygame.transform.flip(frame, True, False)


            # hella magic numbers pls go back
            if self.direction == 1:
                self.hitBox = pygame.Rect(self.x + 64, self.y + 16, 5, 32)
                win.blit(frame, (self.x + 32, self.y + 16))
            else:
                self.hitBox = pygame.Rect(self.x - 32, self.y + 16, 5, 32)
                win.blit(frame, (self.x - 32, self.y + 16))
            #win.blit(frame, self.hitBox)#(self.x + (32 * self.direction), self.y))
        pygame.draw.rect(win, (60,60,60), self.hitBox, 1)



