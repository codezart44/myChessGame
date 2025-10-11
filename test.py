import pygame
import random
pygame.init()

# White pieces
WHITE_PAWN   = pygame.image.load("./pieces/wooden-white/pawn.png")
WHITE_ROOK   = pygame.image.load("./pieces/wooden-white/rook.png")
WHITE_BISHOP = pygame.image.load("./pieces/wooden-white/bishop.png")
WHITE_KNIGHT = pygame.image.load("./pieces/wooden-white/knight.png")
WHITE_QUEEN  = pygame.image.load("./pieces/wooden-white/queen.png")
WHITE_KING   = pygame.image.load("./pieces/wooden-white/king.png")

# Black pieces
BLACK_PAWN   = pygame.image.load("./pieces/wooden-black/pawn.png")
BLACK_ROOK   = pygame.image.load("./pieces/wooden-black/rook.png")
BLACK_BISHOP = pygame.image.load("./pieces/wooden-black/bishop.png")
BLACK_KNIGHT = pygame.image.load("./pieces/wooden-black/knight.png")
BLACK_QUEEN  = pygame.image.load("./pieces/wooden-black/queen.png")
BLACK_KING   = pygame.image.load("./pieces/wooden-black/king.png")

BLACK_SQUARE = pygame.image.load("./board/squares/ornate/black.png")
WHITE_SQUARE = pygame.image.load("./board/squares/outlined/white.png")
FRAME = pygame.image.load("./board/edge/wooden-dark.png")

pos_to_piece = {
    "00": BLACK_ROOK,
    "01": BLACK_KNIGHT,
    "02": BLACK_BISHOP,
    "03": BLACK_QUEEN,
    "04": BLACK_KING,
    "05": BLACK_BISHOP,
    "06": BLACK_KNIGHT,
    "07": BLACK_ROOK,
    "10": BLACK_PAWN,
    "11": BLACK_PAWN,
    "12": BLACK_PAWN,
    "13": BLACK_PAWN,
    "14": BLACK_PAWN,
    "15": BLACK_PAWN,
    "16": BLACK_PAWN,
    "17": BLACK_PAWN,
    "60": WHITE_PAWN,
    "61": WHITE_PAWN,
    "62": WHITE_PAWN,
    "63": WHITE_PAWN,
    "64": WHITE_PAWN,
    "65": WHITE_PAWN,
    "66": WHITE_PAWN,
    "67": WHITE_PAWN,
    "70": WHITE_ROOK,
    "71": WHITE_KNIGHT,
    "72": WHITE_BISHOP,
    "73": WHITE_QUEEN,
    "74": WHITE_KING,
    "75": WHITE_BISHOP,
    "76": WHITE_KNIGHT,
    "77": WHITE_ROOK,
}

SCALE = 4

TILE_SIZE = 16  # 80
RANKS = 8
FILES = 8
EDGE = 8
BOARD_H = RANKS*TILE_SIZE
BOARD_W = FILES*TILE_SIZE
board = pygame.Surface((BOARD_W, BOARD_H))

BOARD_FRAME_W = BOARD_W+2*EDGE
BOARD_FRAME_H = BOARD_H+2*EDGE

WINDOW_H = 600
WINDOW_W = 800

FRAME_X = (WINDOW_W - BOARD_FRAME_W*SCALE) / 2
FRAME_Y = (WINDOW_H - BOARD_FRAME_H*SCALE) / 2
BOARD_X = FRAME_X + EDGE*SCALE
BOARD_Y = FRAME_Y + EDGE*SCALE

window = pygame.display.set_mode((WINDOW_W, WINDOW_H))

# Colors
BLACK = (121,85,72)
WHITE = (255,224,178)
SQUARE_HIGHLIGHT = pygame.image.load("./board/squares/highlight/night-blue.png")
# SQUARE_HIGHLIGHT = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
# SQUARE_HIGHLIGHT.fill((255, 255, 0, 100))


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    mx_board = min((mx - (BOARD_X)), RANKS*TILE_SIZE*SCALE)
    my_board = min((my - (BOARD_Y)), FILES*TILE_SIZE*SCALE)
    mfile = mx_board // (TILE_SIZE*SCALE)
    mrank = my_board // (TILE_SIZE*SCALE)
    print(mfile, mrank)

    for i in range(BOARD_H):
        for j in range(BOARD_W):
            top  = j*TILE_SIZE
            left = i*TILE_SIZE
            square = WHITE_SQUARE if (i+j)%2 == 0 else BLACK_SQUARE
            board.blit(square, (top, left))

            if mfile == j and mrank == i:
                board.blit(SQUARE_HIGHLIGHT, (top, left))

            coord = f"{i}{j}"
            piece = pos_to_piece.get(coord)
            if piece is not None:
                board.blit(piece, (top, left))

    board_scaled = pygame.transform.scale(board, (BOARD_W*SCALE, BOARD_H*SCALE))
    frame_scaled = pygame.transform.scale(FRAME, ((BOARD_FRAME_W*SCALE), (BOARD_FRAME_H*SCALE)))
    window.blit(board_scaled, (BOARD_X, BOARD_Y))
    window.blit(frame_scaled, (FRAME_X, FRAME_Y))
    pygame.display.flip()

pygame.quit()



# 00 01 02 03 04 05 06 07
# 10 11 12 13 14 15 16 17
# 20 21 22 23 24 25 26 27
# 30 31 32 33 34 35 36 37
# 40 41 42 43 44 45 46 47
# 50 51 52 53 54 55 56 57
# 60 61 62 63 64 65 66 67
# 70 71 72 73 74 75 76 77
