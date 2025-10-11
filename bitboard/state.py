from bitboard.constants import *
from bitboard.bitlogic import set_bit, mask_rook_attack_lex, mask_bishop_attack_lex
from bitboard.attack_masks import *
from bitboard.attack_maps import *

class GameState:
    piece_bitboards:list = PIECE_BITBOARDS
    occup_bitboards:list = OCCUPANCY_BITBOARDS
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

        cls.piece_bitboards = [0b0 for _ in range(12)]
        square = 0
        for code in position: 
            if code.isnumeric():
                square += int(code) # increment empty squares
            elif code in ASCII_PIECES[:-1]: # all pieces but .
                piece = ASCII_PIECES.index(code)
                cls.piece_bitboards[piece] = set_bit(cls.piece_bitboards[piece], square)
                square += 1
            assert square <= 64

        cls.occup_bitboards = [0b0 for _ in range(3)]
        for piece in [P,N,B,R,Q,K]: # white pieces
            cls.occup_bitboards[WHITE] |= cls.piece_bitboards[piece]
        for piece in [p,n,b,r,q,k]: # black pieces
            cls.occup_bitboards[BLACK] |= cls.piece_bitboards[piece]
        cls.occup_bitboards[BOTH] = cls.occup_bitboards[WHITE] | cls.occup_bitboards[BLACK]

        cls.side = ['b', 'w'].index(side)
        cls.castling = ''.join([s if s in castling else '-' for s in 'KQkq'])
        cls.enpassant = INDEX_COORD_MAP.index(enpassant)
        cls.half = int(half)
        cls.full = int(full)

    @classmethod
    def reset_state(cls,):
        cls.piece_bitboards:list = PIECE_BITBOARDS
        cls.occup_bitboards:list = OCCUPANCY_BITBOARDS
        cls.side:int = SIDE
        cls.castling:str = CASTLING
        cls.enpassant:int = EN_PASSANT
        cls.half:int = HALF_MOVES
        cls.full:int = FULL_MOVES
    
    @classmethod
    def print_chessboard(cls,):
        """chessboard representation (unicode pieces)"""
        print()
        for i in range(8):
            print(f'{8-i}   ', end='')
            for j in range(8):
                square = 8*i+j
                empty = True
                for piece, bitboard in enumerate(cls.piece_bitboards):
                    if bitboard >> square & 0b1:
                        print(f'{UNICODE_PIECES[piece]}', end=' ')
                        empty = False
                        break
                if empty:
                    print('.', end=' ')
            print()
        print('\n    A B C D E F G H\n')
        print('Side:', ['black', 'white'][cls.side])
        print('EnPa:', INDEX_COORD_MAP[cls.enpassant])
        print('Cast:', cls.castling)
        print(f'Move: {cls.half}h, {cls.full}f')
    
    @classmethod
    def is_squared_attacked(cls, square, side) -> bool:
        """Boolean for whether square is attacked by specified side."""
        if side == BLACK:
            if PAWN_ATTACK_MASKS[WHITE][square] & cls.piece_bitboards[p]: return True
            if KNIGHT_ATTACK_MASKS[square] & cls.piece_bitboards[n]: return True
            if KING_ATTACK_MASKS[square] & cls.piece_bitboards[k]: return True # checks for queen attacks on two lines below vv
            if mask_rook_attack_lex(square, cls.occup_bitboards[BOTH]) & (cls.piece_bitboards[r] | cls.piece_bitboards[q]): return True
            if mask_bishop_attack_lex(square, cls.occup_bitboards[BOTH]) & (cls.piece_bitboards[b] | cls.piece_bitboards[q]): return True
        if side == WHITE:
            if PAWN_ATTACK_MASKS[BLACK][square] & cls.piece_bitboards[P]: return True
            if KNIGHT_ATTACK_MASKS[square] & cls.piece_bitboards[N]: return True
            if KING_ATTACK_MASKS[square] & cls.piece_bitboards[K]: return True # checks for queen attacks on two lines below vv
            if mask_rook_attack_lex(square, cls.occup_bitboards[BOTH]) & (cls.piece_bitboards[R] | cls.piece_bitboards[Q]): return True
            if mask_bishop_attack_lex(square, cls.occup_bitboards[BOTH]) & (cls.piece_bitboards[B] | cls.piece_bitboards[Q]): return True
        return False
    