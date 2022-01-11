"""
Duy Nguyen
1/11/21
"""

import random

import pygame

import constants


class Item(object):
    def __init__(self, itemType):
        self.x = random.randrange(100, constants.WINDOW_WIDTH - 100, 50)
        self.y = -200
        self.vel_y = 0
        self.type = itemType

        self.done = False

        if self.type == "BOXING_GLOVE":
            self.img = pygame.transform.scale(pygame.image.load(constants.IMG_BOXING_GLOVE), (40, 40))
            self.rect = self.img.get_rect()

        elif self.type == "FIREBALL":
            self.img = pygame.transform.scale(pygame.image.load(constants.IMG_FIREBALL), (40, 40))
            self.rect = self.img.get_rect()

    def update(self, win, world):
        dy = 0
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        pygame.draw.rect(win, (255, 255, 255), self.rect, 1) # draws hitbox

        for tile in world.tile_list:

            if tile[1].colliderect(self.rect.x, (self.rect.y + dy), self.rect.width, self.rect.height):
                if self.rect.bottom <= tile[1].bottom:
                    if self.vel_y > 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0

        self.y += dy
        self.rect = pygame.Rect((self.x, self.y), (self.rect.width, self.rect.height))
        if self.y > constants.WINDOW_HEIGHT:
            self.set_done()

        self.weapon_animation(win)

    def weapon_animation(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_weapon_type(self):
        return self.type

    def set_done(self):
        self.done = True

    def get_status(self):
        return self.done