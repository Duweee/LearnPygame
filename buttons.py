"""
Duy Nguyen
1/11/21
"""

import pygame


class Button():
    def __init__(self, x, y, image, scale, type):
        # make sure to pass image in already loaded by pygame
        self.type = type # 0 for button, 1 for label
        self.x = x
        self.y = y
        self.scale = scale # scales button to desired size
        self.width = image.get_width()
        self.height = image.get_height()
        self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))
        # button gets bigger when hovered over
        self.scaledImage = pygame.transform.scale(self.image, (int(self.width * self.scale * 1.1), int(self.height * self.scale * 1.1)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False

    def update(self, win):
        # if clickable button
        if self.type == 0:
            action = False   # turns on when clicked. calls for an action

            pos = pygame.mouse.get_pos()  #position of mouse

            if self.rect.collidepoint(pos):
                # button gets bigger when hovered over
                # compensate coordinates for bigger button
                self.rect.x = self.x + int((self.image.get_width() - self.image.get_width() * 1.1) / 2)
                self.rect.y = self.y + int((self.image.get_height() - self.image.get_height() * 1.1) / 2)
                image = self.scaledImage

                if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                    self.clicked = True
                    action = True
            else:
                image = self.image
                self.rect.topleft = (self.x, self.y)

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # draws button
            win.blit(image, (self.rect.x, self.rect.y))

            # returns whether the button was clicked or not
            return action

        # if just a label
        else:
            win.blit(self.image, (self.rect.x, self.rect.y))

