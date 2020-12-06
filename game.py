import pygame
import random
import math
from pygame import mixer


# player speed(pixel change)
l = 6

# enemy speed(pixel change)
e = 4
ey = 0.1

# bullet speed
b = 10

# enemy no
ne = 10

# inializing the python
pygame.init()

# game winndow
width = 1000
height = 600
screen = pygame.display.set_mode((width, height))

# background
background = pygame.image.load('space.png')
mixer.music.load('bgm.mp3')
mixer.music.play(-1)

# game over
gameover = pygame.image.load('gameover.png')

# tittle and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo2.png')
pygame.display.set_icon(icon)

# player install
playerimg = pygame.image.load("space-ship1.png")
playerX = width / 2 - 32
playerY = height - 98
playerX_change = 0
playerY_change = 0


def player(x, y):
    screen.blit(playerimg, (round(x), round(y)))  # round is just for decimla


# enemy install
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = ne
for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load("skull.png"))
    enemyX.append(random.randint(0, width - 32))
    enemyY.append(random.randint(-100, 200))
    enemyX_change.append(e)
    enemyY_change.append(ey)


def enemy(x, y, i):
    screen.blit(enemyimg[i], (round(x), round(y)))  # round is just for decimls


# bullet install

bulletimg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 0
bullet_state = "ready"
bulletX_change = 0
bulletY_change = b

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 22, bold=True)
textX = 10
textY = 10


def score_val(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (round(x) + 20, round(y) - 35))  # round is just for decimls


# collision
def iscollision(bulletX, bulletY, enemyX, enemyY):
    distance = math.pow(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2), 1 / 2) or -math.pow(
        math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2), 1 / 2)
    if distance > -500 and distance < 16:
        return True
    else:
        return False


# event loop#############################################
running = True
while running:
    # background colour RGB
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # for stabliztaion of game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # key controls
        if event.type == pygame.KEYDOWN:
            # for change in X axis
            if event.key == pygame.K_RIGHT:
                playerX_change = l
            if event.key == pygame.K_LEFT:
                playerX_change = -l
            # for change in Y axis
            if event.key == pygame.K_UP:
                playerY_change = -l
            if event.key == pygame.K_DOWN:
                playerY_change = l
            if event.key == pygame.K_SPACE:
                shoot = mixer.Sound('shoot.wav')
                shoot.play()
                bulletX = playerX
                bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # ....................................
    # bullet and its motion
    if bulletY <= 0:
        bulletX = 0
        bulletY = height - 98
        bullet_state = "ready"

    if bullet_state == "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # captions to control player's controls and boundaries
    playerX += playerX_change
    if playerX >= width - 64:
        playerX = width - 64
    elif playerX <= 0:
        playerX = 0

    player(playerX, playerY)

    # enemy and its motion
    for i in range(num_of_enemies):
        if enemyY[i] > height - 98:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            screen.blit(gameover, (0, 0))

        enemyX[i] += enemyX_change[i]
        if enemyX[i] >= width - 32:
            enemyX_change[i] = -e
        elif enemyX[i] <= 0:
            enemyX_change[i] = e
        enemyY[i] += enemyY_change[i]
        enemy(enemyX[i], enemyY[i], i)
        # collision of bullat and enemy
        collision = iscollision(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            blast = mixer.Sound('blast.wav')
            blast.play()

            bulletY = height - 98
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, width - 32)
            enemyY[i] = random.randint(-100, 200)

    score_val(textX, textY)

    # updation of game window is compulsary
    pygame.display.update()
