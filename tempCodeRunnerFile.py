import pygame
import random

# 128x128 px
TILE_SIZE = 16
BOARD_WIDTH = 8
BOARD_HEIGHT = 8

pygame.init()
screen = pygame.display.set_mode((BOARD_HEIGHT*TILE_SIZE, BOARD_WIDTH*TILE_SIZE))

for i in range(BOARD_HEIGHT):
    for j in range(BOARD_WIDTH):
        color = [random.randint(0, 255)]*3
        rect = pygame.Rect(i*TILE_SIZE, j*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect)
