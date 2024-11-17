from bitboard.constants import *
from bitboard.bitlogic import set_bit

# MOVE COUNTERS
HALF_MOVES = 0
FULL_MOVES = 1
SIDE = WHITE # Side to move
# En Passant
EN_PASSANT = -1 # no square

# CASTLING RIGHTS
# CASTLING = 0b0000 # Init castling rights
# WK, WQ, BK, BQ = 0b0001, 0b0010, 0b0100, 0b1000 # 1, 2, 4, 8
CASTLING = 'KQkq' # KQkq for full castling right, Kq for white king and black queen, - for none

PIECE_BITBOARDS = [ # e.g. PIECE_BITBOARD[R] -> bitboard for white rooks
    # white pieces
    0b00000000_11111111_00000000_00000000_00000000_00000000_00000000_00000000, # P
    0b01000010_00000000_00000000_00000000_00000000_00000000_00000000_00000000, # N
    0b00100100_00000000_00000000_00000000_00000000_00000000_00000000_00000000, # B
    0b10000001_00000000_00000000_00000000_00000000_00000000_00000000_00000000, # R
    0b00001000_00000000_00000000_00000000_00000000_00000000_00000000_00000000, # K
    0b00010000_00000000_00000000_00000000_00000000_00000000_00000000_00000000, # Q
    # black pieces
    0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_00000000, # p
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_01000010, # n
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00100100, # b
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_10000001, # r
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00001000, # q
    0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00010000, # k
    # empty squares
    # 0b00000000_00000000_11111111_11111111_11111111_11111111_00000000_00000000, # .
]
OCCUPANCY_BITBOARDS = [
    0b00000000_00000000_00000000_00000000_00000000_00000000_11111111_11111111, # black
    0b11111111_11111111_00000000_00000000_00000000_00000000_00000000_0000000,  # white 
    0b11111111_11111111_00000000_00000000_00000000_00000000_11111111_11111111, # both
]

class GameState:
    bitboards:list = PIECE_BITBOARDS
    side:int = SIDE
    castling:str = CASTLING
    enpassant:int = EN_PASSANT
    half:int = HALF_MOVES
    full:int = FULL_MOVES

    @classmethod
    def parse_fen(cls, fen:str) -> None:
        """..."""
        # Start FEN: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        position, side, castling, enpassant, half, full = fen.strip().split(' ')

        cls.bitboards = [0b0 for _ in range(12)]
        square = 0
        for code in position: 
            if code.isnumeric():
                square += int(code) # increment empty squares
            elif code in ASCII_PIECES[:-1]: # all pieces but .
                piece = ASCII_PIECES.index(code)
                cls.bitboards[piece] = set_bit(cls.bitboards[piece], square)
                square += 1
            assert square <= 64

        cls.side = ['b', 'w'].index(side)
        cls.castling = castling
        cls.enpassant = INDEX_COORD_MAP.index(enpassant)
        cls.half = int(half)
        cls.full = int(full)

