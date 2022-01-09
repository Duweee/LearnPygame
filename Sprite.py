import random

import constants
import scoreboard
from spritesheet_functions import *
from projectile import *

class Player(object):
    def __init__(self, x, y, width, height, idleIMG, walkIMG, attackIMG, projectileLog):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # for spritesheet and animations
        self.idleIMG = SpriteSheet(idleIMG)
        self.walkIMG = SpriteSheet(walkIMG)
        self.attackIMG = SpriteSheet(attackIMG)
        self.idleCount = 0
        self.walkCount = 0
        # 1 means facing right, -1 means left
        self.direction = 1
        self.moveSpeed = constants.SPRITE_SPEED
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
        self.projectileLog = projectileLog
        # attacking and projectiles and animation
        self.attackDelay = 0
        self.attackBuffer = constants.ATTACK_DELAY
        self.attackCount = 0   # for animation
        self.weapon = "NONE"
        self.weaponCounter = 0  # for weapon ammo percent

        self.dead = False
        self.slideCounter = 0
        self.respawnCounter = 0



    def update(self, win, world):
        if self.weaponCounter <= 0:
            self.weaponCounter = 0
            self.weapon = "NONE"


        self.attackCount += 1
        if (self.attackCount >= 4):
            self.attackCount = 0

        if (self.attackDelay >= 0):
            self.attackDelay -= 1

        self.gravity()

        if (self.slideCounter > 0):
            self.slideCounter -= 1
        if (self.slideCounter < 0):
            self.slideCounter += 1

        self.dx += self.slideCounter * -1

        if self.dead:
            self.respawn()

        # prevents falling through bottom of window. resets jumping
        """if self.y + self.height > constants.WINDOW_HEIGHT:
            self.y = constants.WINDOW_HEIGHT - self.height
            self.dy = 0
            self.isJumping = False"""

        if self.y > constants.WINDOW_HEIGHT:
            self.dead = True
            scoreboard.decrease_lives()

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

        import main
        for item in main.items:
            if item.rect.colliderect(self.rect.x, (self.rect.y + self.dy), self.width, self.height):
                self.weapon = item.get_weapon_type()
                self.weaponCounter = 10
                item.set_done()

        if self.weapon != "NONE":
            self.draw_weapon_durability(win)

        # updates location
        self.x += self.dx
        self.y += self.dy
        self.dx = 0
        self.dy = 0
        # updating hitbox rect
        self.rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        # draw hitbox
        #pygame.draw.rect(win, (255, 255, 255), self.rect, 1)

    def get_sprite_weapon(self):
        return self.weapon

    def takeDamage(self, direction):
        self.slideCounter += 10 * direction

    def attack(self, win):
        if (self.attackDelay <= 0):
            if self.weapon == "BOXING_GLOVE":
                self.projectileLog.new_projectile("BOXING_GLOVE", self.direction, self.x, self.y)
                self.weaponCounter -= 1
            elif self.weapon == "FIREBALL":
                self.projectileLog.new_projectile("FIREBALL", self.direction, self.x, self.y)
                self.weaponCounter -= 1
            else:
                self.projectileLog.new_projectile("", self.direction, self.x, self.y + self.height * 3/5)
                print("X")

            self.attackDelay = self.attackBuffer

    def moveDown(self):
        if (self.phasingCounter <= -10):
            self.isJumpingDown = False
            self.phasingCounter = 0

        if not (self.isJumpingDown):
            self.isJumpingDown = True
            self.phasingCounter = 15


    def moveRight(self):
        self.dx = self.moveSpeed
        self.walkCount += 1
        self.direction = 1

    def moveLeft(self):
        self.dx = -self.moveSpeed
        self.walkCount += 1
        self.direction = -1

    def jump(self):
        if not self.isJumping:
            self.vel_y = -15
            self.isJumping = True

    def gravity(self):
        self.isJumping = True
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy += self.vel_y

    def draw_weapon_durability(self, win):
        pygame.draw.rect(win, (70, 70, 70), ((self.x + self.width + 5, self.y), (5, 2 * self.weaponCounter)))


    def attackAnimation(self, win):
        if self.direction == 1:
            axis = self.attackCount * 32
            frame = self.attackIMG.get_image(axis, 0, 32, 64)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))
        else:
            axis = self.attackCount * 32
            frame = pygame.transform.flip(self.attackIMG.get_image(axis, 0, 32, 64), True, False)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))

    def walkAnimation(self, win):
        if self.walkCount >= 18:
            self.walkCount = 0
        if self.direction == 1:
            temp = self.walkCount // 3
            axis = temp * 32
            frame = self.walkIMG.get_image(axis, 0, 32, 64)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))
            self.walkCount += 1
        else:
            temp = self.walkCount // 3
            axis = temp * 32
            frame = pygame.transform.flip((self.walkIMG.get_image(axis, 0, 32, 64)), True, False)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))
            self.walkCount += 1

    def idleAnimation(self, win):
        if self.idleCount >= 24:
            self.idleCount = 0
        if self.direction == 1:
            temp = self.idleCount // 6
            axis = temp * 32
            frame = self.idleIMG.get_image(axis, 0, 32, 64)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))
            self.idleCount += 1
        else:
            temp = self.idleCount // 6
            axis = temp * 32
            frame = pygame.transform.flip((self.idleIMG.get_image(axis, 0, 32, 64)), True, False)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x - 16, self.y))
            self.idleCount += 1

    def respawn(self):
        if scoreboard.lives > 0:
            if self.respawnCounter < constants.RESPAWN_DELAY:
                self.respawnCounter += 1
                self.y = -100
            else:
                self.x = random.randrange(0, 1050, 1)
                self.y = -100
                self.dead = False
                self.respawnCounter = 0



"""
class Player(object):
    def __init__(self, x, y, width, height, idle, walk):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isJump = False
        self.isWalk = False
        self.jumpCount = 10
        self.dirX = -1
        self.dirY = 1
        self.walkCount = 0
        self.walkIMG = SpriteSheet(walk)
        self.idleIMG = SpriteSheet(idle)
        self.idleTimer = 0
        self.velY = 0
        self.dx = constants.SPRITE_SPEED
        self.dy = 0
        self.rect = pygame.Rect((self.x + 16, self.y), (self.width, self.height))



    def draw(self, win):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        if self.idleTimer + 1 >= 24:
            self.idleTimer = 0


        #gravity
        self.dy = 0
        self.velY += 1
        if self.velY > 10:
            self.velY = 10
        self.dy += self.velY

        if self.dirX == -1 and self.isWalk:
            self.dx = self.dirX * constants.SPRITE_SPEED
            #self.x += self.dx
            temp = self.walkCount // 3
            axis = temp * 32
            frame = pygame.transform.flip((self.walkIMG.get_image(axis, 0, 32, 64)), True, False)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x, self.y))
            self.walkCount += 1
        elif self.dirX == 1 and self.isWalk:
            self.dx = self.dirX * constants.SPRITE_SPEED
            #self.x += self.dx
            temp = self.walkCount // 3
            axis = temp * 32
            frame = self.walkIMG.get_image(axis, 0, 32, 64)
            frame = pygame.transform.scale2x(frame)
            win.blit(frame, (self.x, self.y))
            self.walkCount += 1
        else:
            self.dx = 0
            if self.dirX == -1:
                temp = self.idleTimer // 6
                axis = temp * 32
                frame = pygame.transform.flip((self.idleIMG.get_image(axis, 0, 32, 64)), True, False)
                frame = pygame.transform.scale2x(frame)
                win.blit(frame, (self.x, self.y))
                self.idleTimer += 1
            else:
                temp = self.idleTimer // 6
                axis = temp * 32
                frame = self.idleIMG.get_image(axis, 0, 32, 64)
                frame = pygame.transform.scale2x(frame)
                win.blit(frame, (self.x, self.y))
                self.idleTimer += 1

        if self.y + self.height + self.dy > constants.WINDOW_HEIGHT:
            self.y = constants.WINDOW_HEIGHT - self.height
            self.dy = 0

        self.y += self.dy

        self.rect = pygame.Rect((self.x + 16, self.y), (self.width, self.height))
        pygame.draw.rect(win, (255, 255, 255), self.rect, 1)

        self.x += self.dx

    def sprite_jump(self, win):
        self.velY = -15
        
        """
"""
        if self.jumpCount >= -10:
            self.dirY = 1
            if self.jumpCount < 0:
                self.dirY = -1

            self.y -= self.jumpCount

            self.jumpCount -= 1
            self.draw(win)
        else:
            self.isJump = False
            self.jumpCount = 10


        pygame.display.update()
"""
