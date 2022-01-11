"""
Duy Nguyen
1/11/21
"""

import pygame

import constants

score = 0
lives = constants.STARTING_LIVES


def draw_scoreBoard(win, score, x, y, scale):
    scoreFont = pygame.font.SysFont('impact', 30 * scale)

    text = scoreFont.render('Lives: ' + str(lives) + '      Score: ' + str(score), 1, (0, 0, 0))
    win.blit(text, (x, y))

def draw_score(win, x, y, scale):
    scoreFont = pygame.font.SysFont('impact', 30 * scale)
    text = scoreFont.render(str(score), 1, (0, 0, 0))
    textRect = text.get_rect()

    win.blit(text, (x, y))


def reset_score():
    global score
    score = 0

def reset_lives():
    global lives
    lives = constants.STARTING_LIVES

def increase_score():
    global score
    score += 1


def decrease_lives():
    global lives
    lives -= 1
