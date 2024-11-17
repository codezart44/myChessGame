from bitboard.constants import *    # main import from notation.py
from bitboard.state import GameState


# chessboard representation (unicode pieces)
def print_chessboard():
    """..."""
    print()
    for i in range(8):
        print(f'{8-i}   ', end='')
        for j in range(8):
            square = 8*i+j
            empty = True
            for piece, bitboard in enumerate(GameState.bitboards):
                if bitboard >> square & 0b1:
                    print(f'{UNICODE_PIECES[piece]}', end=' ')
                    empty = False
                    break
            if empty:
                print('.', end=' ')
        print()
    print('\n    A B C D E F G H\n')
    print('Side:', ['black', 'white'][GameState.side])
    print('EnPa:', INDEX_COORD_MAP[GameState.enpassant])
    print('Cast:', GameState.castling)
    print(f'Move: {GameState.half}h, {GameState.full}f')



def main():
    print_chessboard()


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