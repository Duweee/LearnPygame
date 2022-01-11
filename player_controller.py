"""
Duy Nguyen
1/11/21
"""

import pygame


def keyboardListener(pinkSprite, win):
    key = pygame.key.get_pressed()
    events = pygame.event.get()

    if key[pygame.K_UP]:
        pinkSprite.jump()
    if key[pygame.K_DOWN]:
        pinkSprite.moveDown()
    if key[pygame.K_SPACE]:
        pinkSprite.attack(win)
        if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
            pinkSprite.attackAnimation(win)
    if key[pygame.K_RIGHT]:
        pinkSprite.moveRight()
        pinkSprite.walkAnimation(win)
    elif key[pygame.K_LEFT]:
        pinkSprite.moveLeft()
        pinkSprite.walkAnimation(win)
    if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_SPACE]:
        pinkSprite.idleAnimation(win)



"""import pygame
import constants
from Sprite import Player


class PlayerController(object):
    def __init__(self, pink, white):
        self.pink = pink
        self.white = white

    def update(self, win, env):
        keys = pygame.key.get_pressed()

        for tile in env.tile_list:
            if tile.colliderect(self.pink.x + 16, self.pink.y + self.pink.dy, self.pink.width, self.pink.height):
                if self.pink.velY > 0:
                    self.pink.y = tile.y - self.pink.height
                    self.pink.velY = 0
                if self.pink.velY < 0:
                    self.pink.y = tile.y + constants.TILE_SIZE
                    self.pink.velY = 0
            if tile.colliderect(self.pink.x + 16 + self.pink.dx, self.pink.y, self.pink.width, self.pink.height):
                self.pink.dx = 0




        if keys[pygame.K_LEFT] and self.pink.x > 0:
            #self.pink.x -= constants.SPRITE_SPEED
            self.pink.dirX = -1
            self.pink.isWalk = True

        elif keys[pygame.K_RIGHT] and self.pink.x < constants.WINDOW_WIDTH - self.pink.width:
            #self.pink.x += constants.SPRITE_SPEED
            self.pink.dirX = 1
            self.pink.isWalk = True

        else:
            self.pink.isWalk = False

        if keys[pygame.K_UP] and not self.pink.isJump:
            self.pink.sprite_jump(win)
            self.pink.isJump = True
        if not keys[pygame.K_UP]:
            self.pink.isJump = False
        """"""if not self.pink.isJump:
            if keys[pygame.K_UP]:
                self.pink.isJump = True
        else:
            self.pink.sprite_jump(win)"""
"""
        if keys[pygame.K_a] and self.white.x > 0:
            self.white.x -= constants.SPRITE_SPEED
            self.white.dirX = -1
            self.white.isWalk = True

        elif keys[pygame.K_d] and self.white.x < constants.WINDOW_WIDTH - self.white.width:
            self.white.x += constants.SPRITE_SPEED
            self.white.dirX = 1
            self.white.isWalk = True

        else:
            self.white.isWalk = False

        if not self.white.isJump:
            if keys[pygame.K_w]:
                self.white.isJump = True
        else:
            self.white.sprite_jump(win)

"""
