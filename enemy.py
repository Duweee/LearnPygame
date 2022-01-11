import constants
import scoreboard
from Sprite import Player
from spritesheet_functions import *
import random

class Enemy(Player):
    def __init__(self, x, y, width, height, idleIMG, projectileLog):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #for animation
        self.idleIMG = SpriteSheet(idleIMG)
        self.deathIMG = SpriteSheet(constants.IMG_SLIME_DEATH)
        self.idleCount = 0
        self.walkCount = 0
        self.deathCount = 0
        # 1 means facing right, -1 means left
        self.direction = 1
        # accounts for gravity and jumping
        self.vel_y = 0
        # change in x or y per update
        self.dx = 0
        self.dy = 0
        # prevents double jumping, sprite cannot jump if it is
        # already jumping
        self.isJumping = False
        # used to phase down platforms
        self.isJumpingDown = False
        self.phasingCounter = 0
        # hitbox
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.moveSpeed = 2
        self.dying = False
        self.dead = False
        self.projectileLog = projectileLog
        # for sliding when hit by projectile
        self.slideCounter = 0

    def update(self, win, world):

        self.gravity()
        if (self.slideCounter > 0):
            self.slideCounter -= 1

        self.dx += self.slideCounter * self.direction * -1

        if (self.y < 0):
            self.drawIndicator(win)

        # prevents falling through bottom of window. resets jumping
        """if self.y + self.height > constants.WINDOW_HEIGHT:
            self.y = constants.WINDOW_HEIGHT - self.height
            self.dy = 0
            self.isJumping = False"""
        if self.y > constants.WINDOW_HEIGHT:
            self.dead = True
            scoreboard.increase_score()

        # prevents walking past left or right of window
        if self.x + self.dx > constants.WINDOW_WIDTH - self.width or self.x + self.dx < 0:
            self.dx = 0

        # checks for collision with tiles on map
        for tile in world.tile_list:
            # collision with tiles in x axis
            """ if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
                if self.direction == 1:
                    self.x = tile[1].x - self.width
                else:
                    self.x = tile[1].x + constants.TILE_SIZE"""
            if tile[1].colliderect(self.rect.x, (self.rect.y + self.dy), self.width, self.height):

                if (self.phasingCounter > 0):
                    self.phasingCounter -= 1
                    # colliding when falling
                else:
                    if self.rect.bottom <= tile[1].bottom:
                        if self.vel_y > 0:
                            self.dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.isJumping = False
                            self.phasingCounter -= 1

        # updates location
        self.x += self.dx
        self.y += self.dy
        self.dx = 0
        self.dy = 0
        # updating hitbox rect
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        # draw hitbox
        #pygame.draw.rect(win, (255, 255, 255), self.rect, 1)

    def act(self, target, win):
        if self.dying:
            self.deathAnimation(win)
            if self.deathCount >= 14:
                self.dead = True
                self.deathCount = 0

        else:
            if target.y + target.height < self.y + self.height:
                if (random.randrange (1, 10, 1) == 3):
                    self.jump()
            elif target.y + target.height > self.y + self.height and not self.isJumping:
                if (random.randrange(1, 10, 1) == 3):
                    self.moveDown()

            if target.x < self.x:
                self.moveLeft()
            else:
                self.moveRight()

            if self.rect.colliderect(target):
                self.dying = True
                if (self.x > target.x):
                    target.takeDamage(1)
                else:
                    target.takeDamage(-1)

                scoreboard.decrease_lives()

            self.idleAnimation(win)

        for p in self.projectileLog.projectileLog:
            if self.rect.colliderect(p.hitBox):
                self.slideCounter += p.damage


    def deathAnimation(self, win):
        axis = (self.deathCount // 2) * 64 + 384
        frame = self.deathIMG.get_image(axis, 0, 64, 64)
        frame = pygame.transform.scale2x(frame)
        win.blit(frame, (self.x - 48, self.y - 64))
        self.deathCount += 1

    def idleAnimation(self, win):
        if self.idleCount >= 25:
            self.idleCount = 0

        temp = self.idleCount // 5
        axis = temp * 64 + 16
        frame = self.idleIMG.get_image(axis, 32, 32, 32)
        frame = pygame.transform.scale2x(frame)
        win.blit(frame, (self.x - 16, self.y))
        self.idleCount += 1

    def drawIndicator(self, win):
        frame = pygame.transform.scale2x(constants.IMG_RED_ARROW)
        win.blit(constants.IMG_RED_ARROW, (self.x, 10))