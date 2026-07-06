from chess.modules.constants import *    # main import from notation.py
from chess.modules.state import GameState
from chess.modules.blocking import print_bitboard, mask_knight_attack
import random


def main():

    print_bitboard(mask_knight_attack(E4))

    quit()
    fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'
    GameState.parse_fen(fen)
    GameState.print_chessboard()
    is_attacked = GameState.is_squared_attacked(F8, WHITE)
    print(is_attacked)
    


    # print_bitboard(GameState.occup_bitboards[WHITE])
    # print_bitboard(GameState.occup_bitboards[BLACK])
    # print_bitboard(GameState.occup_bitboards[BOTH])


if __name__=='__main__':
    main()





# DEPRECATED


# def mask_bishop_attack(sqr, block):
#     """compute a mask for the squares attacked by a bishop at position sqr"""
#     assert 0 <= sqr <= 63
#     attack = EMPTY
#     rank, file = sqr//8, sqr%8
#     for n in range(4): # four diagonal directions
#         dr = (-1)**n      # 1, -1,  1, -1
#         df = (-1)**(n//2) # 1,  1, -1, -1
#         rank += dr # init one step
#         file += df # ...
#         while 0 <= rank <= 7 and 0 <= file <= 7: # board edges (8x8)
#             attack |= 0b1 << rank*8+file
#             if (0b1 << rank*8+file & block): break # break if obstructing piece
#             rank += dr
#             file += df
#         rank, file = sqr//8, sqr%8 # reset position before next diagonal
    
#     return attack

# def mask_rook_attack(sqr, block):
#     """compute a mask for the squares attacked by a rook at position sqr"""
#     assert 0 <= sqr <= 63
#     attack = EMPTY
#     rank, file = sqr//8, sqr%8
#     for n in range(4): # four orthogonal directions
#         dr = (-1)**n * (1-n//2) # 1, -1, 0,  0
#         df = (-1)**n * (n//2)   # 0,  0, 1, -1
#         rank += dr # init one step
#         file += df # ...
#         while 0 <= rank <= 7 and 0 <= file <= 7: # board edges (8x8)
#             attack |= 0b1 << rank*8+file
#             if (0b1 << rank*8+file & block): break # break if obstructing piece
#             rank += dr
#             file += df
#         rank, file = sqr//8, sqr%8 # reset position before next orthogonal
#     return attack


# def count_bits64(bitboard): # NOTE Use count_bits8 instead!
#     """DEPRECATED count the number of active bits in board bit for bit"""
#     counter = 0
#     while bitboard:
#         if (bitboard & 0b1): counter += 1
#         bitboard >>= 1
#     return counter