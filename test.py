# TEST DOC
import numpy as np
import pandas as pd

# # board state, ctmm, catling rights, en passent, half move clock, full move clock (incremented after blacks move)
# FEN_start = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
# components = FEN_start.split(' ')
# print(components)

# squares = np.array(['.' for _ in range(64)], dtype=object)
# i = 0
# for char in components[0]:
#     if char.isalpha():
#         squares[i] = char
#         i += 1
#     if char.isnumeric():
#         i += int(char)

# board = squares.reshape(8, 8)
# print(board)

target = 0
assert target