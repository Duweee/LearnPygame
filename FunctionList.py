import pygame

from main import *


def redrawGameWindow(win):
    win.fill((0, 0, 0))
    pinkSprite.draw(win)
    pygame.display.update()
