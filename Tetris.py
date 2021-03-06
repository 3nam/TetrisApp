# ===============================================================================================#
# Name        : Tetris.py                                                                       #
# Description : Tetris version of the snake game.                                               #
# Author      : Nguyen Hoang Nam                                                                #
# Date        : 07.11.2017                                                                      #
# ===============================================================================================#

import pygame
import bricks
import time  #
import os  #
import sys

from colors import *

# game stats
WIDTH = 10
HEIGHT = 20
RESWIDTH = WIDTH + 13
RESHEIGHT = HEIGHT + 2
FPS = 40  # frame
GAMESPEED = 500  # milisecond
BLOCK_SIZE = 30
BLOCK_SIZE_INNER = 20
SCORECOEFFICIENT = [1, 3, 5, 10]
# defining the blocks
wallblock = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
wallblock.set_alpha(255)
wallblock.fill(BLUE)
wallblockdark = pygame.Surface((BLOCK_SIZE_INNER, BLOCK_SIZE_INNER))
wallblockdark.set_alpha(255)
wallblockdark.fill(BLUE_DARK)
backblock = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE))
backblock.set_alpha(255)
backblock.fill(BLACK)
brickblock = pygame.Surface((BLOCK_SIZE_INNER, BLOCK_SIZE_INNER))
wallblockdark.set_alpha(255)


# ================================================================================================#
#                                       Function Definitions                                     #
# ================================================================================================#

# draw walls
def drawWalls(surface):
    # left and right walls
    for y in range(HEIGHT + 1):
        surface.blit(wallblock, (0, y * BLOCK_SIZE))
        surface.blit(wallblockdark, (5, y * BLOCK_SIZE + 5))
        surface.blit(wallblock, ((WIDTH + 1) * BLOCK_SIZE, y * BLOCK_SIZE))
        surface.blit(wallblockdark, ((WIDTH + 1) * BLOCK_SIZE + 5, y * BLOCK_SIZE + 5))

    # upper and bottom walls
    for x in range(WIDTH + 2):
        surface.blit(wallblock, (x * BLOCK_SIZE, 0))
        surface.blit(wallblockdark, (x * BLOCK_SIZE + 5, 5))
        surface.blit(wallblock, (x * BLOCK_SIZE, (HEIGHT + 1) * BLOCK_SIZE,))
        surface.blit(wallblockdark, (x * BLOCK_SIZE + 5, (HEIGHT + 1) * BLOCK_SIZE + 5))

    # left and right box
    for y in range(8):
        surface.blit(wallblock, ((WIDTH + 3) * BLOCK_SIZE, (y + 2) * BLOCK_SIZE))
        surface.blit(wallblockdark, ((WIDTH + 3) * BLOCK_SIZE + 5, (y + 2) * BLOCK_SIZE + 5))
        surface.blit(wallblock, ((WIDTH + 11) * BLOCK_SIZE, (y + 2) * BLOCK_SIZE))
        surface.blit(wallblockdark, ((WIDTH + 11) * BLOCK_SIZE + 5, (y + 2) * BLOCK_SIZE + 5))

    # upper and bottom box
    for x in range(9):
        surface.blit(wallblock, ((x + WIDTH + 3) * BLOCK_SIZE, 2 * BLOCK_SIZE))
        surface.blit(wallblockdark, ((x + WIDTH + 3) * BLOCK_SIZE + 5, 2 * BLOCK_SIZE + 5))
        surface.blit(wallblock, ((x + WIDTH + 3) * BLOCK_SIZE, 10 * BLOCK_SIZE))
        surface.blit(wallblockdark, ((x + WIDTH + 3) * BLOCK_SIZE + 5, 10 * BLOCK_SIZE + 5))


def drawPlayGround(surface, playGround, nextBrick, score):
    surface.fill(BLACK)
    drawWalls(surface)
    for i in range(len(playGround)):
        for j in range(len(playGround[i])):
            brickblock.fill(color[playGround[i][j]])
            surface.blit(brickblock, ((j + 1) * BLOCK_SIZE + 5, (i + 1) * BLOCK_SIZE + 5))
    brickblock.fill(color[nextBrick.type])
    for i in range(len(nextBrick.shape)):
        for j in range(len(nextBrick.shape[i])):
            if nextBrick.shape[i][j]:
                surface.blit(brickblock, ((WIDTH + 6 + j) * BLOCK_SIZE + 5, (i + 5) * BLOCK_SIZE + 5))
    scoretext = fontLarge.render(str(score), 1, color[len(str(score)) + 3])
    surface.blit(scoretext0, ((WIDTH + 6) * BLOCK_SIZE, 14 * BLOCK_SIZE))
    surface.blit(scoretext, ((WIDTH + 7) * BLOCK_SIZE - len(str(score)) * 12, 16 * BLOCK_SIZE))
    pygame.display.flip()


def deleteBrick(playGround, brk):
    for i in range(len(brk.shape)):
        for j in range(len(brk.shape[i])):
            if brk.shape[i][j]:
                playGround[brk.position[0] + i][brk.position[1] + j] = 0


def updateBrick(playGround, brk):
    for i in range(len(brk.shape)):
        for j in range(len(brk.shape[i])):
            if brk.shape[i][j]:
                playGround[brk.position[0] + i][brk.position[1] + j] = brk.type


def isLegit(brick, brick1, playGround):
    posList = [[]]
    for i in range(len(brick.shape)):
        for j in range(len(brick.shape[i])):
            if brick.shape[i][j]:
                posList.append([brick.position[0] + i, brick.position[1] + j])
    for i in range(len(brick1.shape)):
        for j in range(len(brick1.shape[i])):
            if brick1.shape[i][j]:
                if brick1.position[1] + j >= WIDTH or brick1.position[1] + j < 0 or brick1.position[
                    0] + i >= HEIGHT or (
                    playGround[brick1.position[0] + i][brick1.position[1] + j] and not [brick1.position[0] + i,
                                                                                        brick1.position[
                                                                                            1] + j] in posList):
                    return False
    return True


# ================================================================================================#
#                                       Main Game Part                                           #
# ================================================================================================#

# Init game
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(((RESWIDTH) * BLOCK_SIZE, RESHEIGHT * BLOCK_SIZE))
pygame.display.set_caption("Tetris")
fontSmall = pygame.font.SysFont(pygame.font.get_default_font(), 25)
fontMedium = pygame.font.SysFont(pygame.font.get_default_font(), 40)
fontLarge = pygame.font.SysFont(pygame.font.get_default_font(), 120)
starttext0 = fontLarge.render("TETRIS", 1, WHITE)
starttext = fontSmall.render("PRESS ANY KEY TO START...", 1, WHITE)
gameovertext = fontMedium.render("GAME OVER", 1, WHITE)
scoretext0 = fontMedium.render("SCORE", 1, WHITE)
scoretext = fontLarge.render("0", 1, WHITE)
# press any key to start!!!
screen.fill(BLACK)
screen.blit(starttext0, ((RESWIDTH - 10) * BLOCK_SIZE // 2, (RESHEIGHT - 6) * BLOCK_SIZE // 2))
screen.blit(starttext, ((RESWIDTH - 8) * BLOCK_SIZE // 2, RESHEIGHT * BLOCK_SIZE // 2))
pygame.display.flip()
waiting = True
while waiting:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        sys.exit()
    elif event.type == pygame.KEYDOWN:
    	if event.key == pygame.K_ESCAPE:
    		sys.exit()
    	else: waiting = False

#
drawWalls(screen)
playGround = [[0] * WIDTH for i in range(HEIGHT)]
#GAME HACKING
playGround[HEIGHT - 4] = [1, 3, 3, 2, 6, 4, 4, 7, 5, 0]
playGround[HEIGHT - 3] = [3, 3, 1, 5, 1, 4, 4, 7, 7, 0]
playGround[HEIGHT - 2] = [1, 3, 2, 1, 6, 4, 4, 7, 5, 0]
playGround[HEIGHT - 1] = [3, 3, 1, 1, 5, 4, 4, 7, 7, 0]
playGround[HEIGHT - 4] = playGround[HEIGHT - 4] + [0] * (WIDTH - len(playGround[HEIGHT - 4]))
playGround[HEIGHT - 3] = playGround[HEIGHT - 3] + [0] * (WIDTH - len(playGround[HEIGHT - 3]))
playGround[HEIGHT - 2] = playGround[HEIGHT - 2] + [0] * (WIDTH - len(playGround[HEIGHT - 2]))
playGround[HEIGHT - 1] = playGround[HEIGHT - 1] + [0] * (WIDTH - len(playGround[HEIGHT - 1]))
#END GAME HACKING
continueGame = True
score = 0
frame = 1
nextBrick = bricks.brick(WIDTH)
nextBrick.type = 7
nextBrick.shape = nextBrick.bricksShape[nextBrick.type]
while continueGame:
    # Create new brick
    brk = nextBrick
    nextBrick = bricks.brick(WIDTH)
    pos = 0
    for i in range(len(brk.shape)):
        for j in range(len(brk.shape[i])):
            if brk.shape[i][j] and playGround[brk.position[0] + i][brk.position[1] + j]:
                pos = i
                continueGame = False
    if not continueGame:
        break

    for i in range(len(brk.shape)):
        for j in range(len(brk.shape[i])):
            if brk.shape[i][j]:
                playGround[brk.position[0] + i][brk.position[1] + j] = brk.type
    drawPlayGround(screen, playGround, nextBrick, score)
    down=False
    #Falling
    while True:
        if not down:
            frame = (frame + 1) % (FPS * GAMESPEED / 1000)
            #Event input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()
                    elif event.key == pygame.K_UP:
                        futureBrick = bricks.brick(WIDTH)
                        bricks.brick.__eq__(futureBrick, brk)
                        futureBrick.rotate()
                        if isLegit(brk, futureBrick, playGround):
                            deleteBrick(playGround, brk)
                            brk = futureBrick
                            updateBrick(playGround, brk)
                            drawPlayGround(screen, playGround, nextBrick, score)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    	down = True
                    elif event.key == pygame.K_DOWN:
                        frame = 0
                        break
                    elif event.key == pygame.K_RIGHT:
                        futureBrick = bricks.brick(WIDTH)
                        bricks.brick.__eq__(futureBrick, brk)
                        futureBrick.moveRight()
                        if isLegit(brk, futureBrick, playGround):
                            deleteBrick(playGround, brk)
                            brk = futureBrick
                            updateBrick(playGround, brk)
                            drawPlayGround(screen, playGround, nextBrick, score)
                    elif event.key == pygame.K_LEFT:
                        futureBrick = bricks.brick(WIDTH)
                        bricks.brick.__eq__(futureBrick, brk)
                        futureBrick.moveLeft()
                        if isLegit(brk, futureBrick, playGround):
                            deleteBrick(playGround, brk)
                            brk = futureBrick
                            updateBrick(playGround, brk)
                        drawPlayGround(screen, playGround, nextBrick, score)
        if frame==0 or down:
            #isCollision
            futureBrick = bricks.brick(WIDTH)
            bricks.brick.__eq__(futureBrick, brk)
            futureBrick.fall()
            if not isLegit(brk, futureBrick, playGround):
                for i in range(HEIGHT):
                    if not 0 in playGround[i]:
                        combo = 1
                        for j in range(i + 1, HEIGHT):
                            if not 0 in playGround[j]:
                                combo += 1
                        print("Combo " + str(combo) + "!")
                        score += int(SCORECOEFFICIENT[combo - 1] * 50 * (GAMESPEED / 1000.0))
                        for j in range(HEIGHT):
                            if not 0 in playGround[j]:
                                for q in range(1, j + 1)[::-1]:
                                    playGround[q] = playGround[q - 1][:]
                                playGround[0] = ([0] * WIDTH)
            	#New brick
                break
            else:
            	#Brick fall
            	deleteBrick(playGround, brk)
            	brk.fall()
            	updateBrick(playGround, brk)
            	drawPlayGround(screen, playGround, nextBrick, score)
        clock.tick(FPS)

    #isFull = game over
    for i in range(WIDTH):
        if playGround[i]:
            break;

# endgame
screen.fill(BLACK)
while True:
    screen.blit(gameovertext, ((RESWIDTH - 5) * BLOCK_SIZE // 2, (RESHEIGHT - 2) * BLOCK_SIZE // 2))
    pygame.display.flip()
    event = pygame.event.wait()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        else:
            break;
    elif event.type == pygame.QUIT:
        sys.exit()