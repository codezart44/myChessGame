from src.chess.bitboard.constants import *
from src.chess.bitboard.bits import BitOperations as bop
from src.chess.bitboard.attacks import AttackMasks as masks

class GameState:
    piece_bitboards:list = PIECE_BITBOARDS.copy()
    occup_bitboards:list = OCCUPANCY_BITBOARDS.copy()
    side:int = SIDE
    castling:str = CASTLING
    enpassant:int = EN_PASSANT
    half:int = HALF_MOVES
    full:int = FULL_MOVES

    @classmethod
    def reset_state(cls,):
        cls.piece_bitboards:list = PIECE_BITBOARDS
        cls.occup_bitboards:list = OCCUPANCY_BITBOARDS
        cls.side:int = SIDE
        cls.castling:str = CASTLING
        cls.enpassant:int = EN_PASSANT
        cls.half:int = HALF_MOVES
        cls.full:int = FULL_MOVES
    
