from chess.modules.bits import BitOperations as bop
from chess.modules.constants import *


def fen_to_bitboards(fen:str) -> None:
    """..."""
    # Start FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
    position = fen.strip().split(' ')[0]

    piece_bitboards = [0b0 for _ in range(12)]
    square = 0
    for code in position: 
        if code.isnumeric():
            square += int(code) # increment empty squares
        elif code in ASCII_PIECES[:-1]: # all pieces but .
            piece = ASCII_PIECES.index(code)
            piece_bitboards[piece] = bop.set_bit(piece_bitboards[piece], square)
            square += 1
        assert square <= 64

    color_bitboards = piece_to_color_bitboards(piece_bitboards)
    return piece_bitboards, color_bitboards

def piece_to_color_bitboards(piece_bitboards) -> list:
    color_bitboards = [0b0 for _ in range(3)]
    for piece in [P,N,B,R,Q,K]: # white pieces
        color_bitboards[WHITE] |= piece_bitboards[piece]
    for piece in [p,n,b,r,q,k]: # black pieces
        color_bitboards[BLACK] |= piece_bitboards[piece]
    color_bitboards[BOTH] = color_bitboards[WHITE] | color_bitboards[BLACK]
    return color_bitboards

    # position, side, castling, enpassant, half, full = fen.strip().split(' ')[0]
    # cls.side = ['b', 'w'].index(side)
    # cls.castling = ''.join([s if s in castling else '-' for s in 'KQkq'])
    # cls.enpassant = INDEX_COORD_MAP.index(enpassant)
    # cls.half = int(half)
    # cls.full = int(full)


def print_chessboard(piece_bitboards):
    """chessboard representation (unicode pieces)"""
    print()
    for i in range(8):
        print(f'{8-i}   ', end='')
        for j in range(8):
            square = 8*i+j
            empty = True
            for piece, bitboard in enumerate(piece_bitboards):
                if bitboard >> square & 0b1:
                    print(f'{UNICODE_PIECES[piece]}', end=' ')
                    empty = False
                    break
            if empty:
                print('.', end=' ')
        print()
    print('\n    A B C D E F G H\n')
    # print('Side:', ['black', 'white'][side])
    # print('EnPa:', INDEX_COORD_MAP[enpassant])
    # print('Cast:', castling)
    # print(f'Move: {half}h, {full}f')


def print_bitboard(bitboard):
    """bitboard terminal representation"""
    print()
    for i in range(8):
        print(f'{8-i}   ', end='')
        for j in range(8):
            index = i*8+j
            print(f'{bitboard >> index & 0b1} ', end='')
        print()
    print('\n    A B C D E F G H\n')
    print(f'    bitboard: {bitboard}d\n')



