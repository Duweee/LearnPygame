"""
Duy Nguyen
1/11/21
"""

from player_controller import *
from Sprite import *
from buttons import *
from weapons import *
from world import *
from enemy import *
import constants
import scoreboard


def redraw_game_window():
    win.blit(background, (0, 0))
    world.draw(win)

    scoreboard.draw_scoreBoard(win, scoreboard.score, 800, 20, 1)

    projectileLog.update(win)

    keyboardListener(pinkSprite, win)
    pinkSprite.update(win, world)
    for slime in slimes:
        slime.update(win, world)
        if slime.dead == True:
            slimes.pop(slimes.index(slime))
        slime.act(pinkSprite, win)

    for item in items:
        item.update(win, world)
        if item.get_status():
            items.pop(items.index(item))

    pygame.display.update()


def reset_game():
    scoreboard.reset_score()
    scoreboard.reset_lives()
    pinkSprite.respawn()
    for slime in slimes:
        slimes.pop(slimes.index(slime))


def start_menu():
    global gameMode
    win.fill((180, 160, 220))
    scoreLabel.update(win)
    blankScoreLabel.update(win)
    scoreboard.draw_score(win, blankScoreLabel.x + 100, blankScoreLabel.y + 8, 3)
    if startButton.update(win):
        reset_game()
        gameMode = "GAME"
    draw_menu_character()
    pygame.display.update()


def start_game():
    # these loops need to be moved to a game clock function
    rng = random.randrange(0, 10, 1)
    if len(slimes) < constants.MAX_NUM_SLIMES:
        slimes.append(Enemy(random.randrange(0, 1050, 1), random.randrange(150, 600, 50) * -1, 32, 32, constants.IMG_SLIME_MOVE, projectileLog))
    elif len(slimes) > constants.MAX_NUM_SLIMES:
        slimes.pop(0)
    if len(items) < constants.MAX_ITEMS:
        if rng == 1:
            items.append(Item("BOXING_GLOVE"))
        elif rng == 2:
            items.append(Item("FIREBALL"))

    if scoreboard.score >= 15:
        constants.MAX_NUM_SLIMES = 8
    elif scoreboard.score >= 8:
        constants.MAX_NUM_SLIMES = 6
    elif scoreboard.score >= 2:
        constants.MAX_NUM_SLIMES = 4
    else:
        constants.MAX_NUM_SLIMES = 2

    if scoreboard.lives <= 0:
        global gameMode
        gameMode = "MENU"
    redraw_game_window()


def draw_menu_character():      # super duper brute forced go fix this
    global menuCounter
    if menuCounter >= 20:
        menuCounter = 0
    else:
        menuCounter += 1
    axis = menuCounter // 6 * 32
    frame = pygame.transform.flip((menuAnimation.get_image(axis, 0, 32, 64)), True, False)

    frame = pygame.transform.scale(frame, (32 * 10, 64 * 10))
    win.blit(frame, (680, 100))
    pygame.draw.rect(win, "BLACK", pygame.Rect((760, 420), (180,30)))

pygame.init()
background = constants.IMG_BACKGROUND
clock = pygame.time.Clock()
win = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
pygame.display.set_caption("Sprite Survival")


# initializations
menuAnimation = SpriteSheet(constants.IMG_PINK_IDLE) # pink sprite on menu
menuCounter = 0

gameMode = "MENU"
projectileLog = ProjectileLog()

startButton = Button(180, constants.WINDOW_HEIGHT - 270, constants.IMG_START_LABEL, 6, 0)
scoreLabel = Button(100, 120, constants.IMG_SCORE_LABEL, 4, 1)
blankScoreLabel = Button(400, 110, constants.IMG_BLANK_LABEL, 4, 1)

pinkSprite = Player(300, 400, 32, 64, constants.IMG_PINK_IDLE, constants.IMG_PINK_WALK, constants.IMG_PINK_ATTACK, projectileLog)
world = World(constants.WORLD_DATA)
slimes = []
character = []
items = []


# main loop
running = True
while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if gameMode == "GAME":
        start_game()
    if gameMode == "MENU":
        start_menu()

        """if len(slimes) < constants.MAX_NUM_SLIMES:
            slimes.append(Enemy(random.randrange(0, 1050, 1), -200, 32, 32, constants.IMG_SLIME_MOVE, projectileLog))
        if scoreboard.lives == 0:
            gameMode = "MENU"
        redrawGameWindow()"""


pygame.quit()
