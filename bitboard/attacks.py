from constants import *
from bits import BitOperations as bop
from lookup.attack_masks import (
    PAWN_ATTACK_MASKS,
    KNIGHT_ATTACK_MASKS,
    KING_ATTACK_MASKS,
    BISHOP_ATTACK_MASKS,
    ROOK_ATTACK_MASKS,
)
from lookup.attack_maps import (
    BISHOP_OCCUPANCY_ATTACK_MAP,
    ROOK_OCCUPANCY_ATTACK_MAP,
)

def squared_attacked_by(sqr, color, piece_bitboards, color_bitboards) -> bool:
    """Boolean for whether square is attacked by specified side."""
    if color == BLACK:
        if AttackMasks.pawn(sqr, WHITE)                   & piece_bitboards[p]: return True
        if AttackMasks.knight(sqr)                        & piece_bitboards[n]: return True
        if AttackMasks.king(sqr)                          & piece_bitboards[k]: return True
        if AttackMasks.rook(sqr, color_bitboards[BOTH])   & piece_bitboards[r]: return True
        if AttackMasks.bishop(sqr, color_bitboards[BOTH]) & piece_bitboards[b]: return True
        if AttackMasks.queen(sqr, color_bitboards[BOTH])  & piece_bitboards[q]: return True
    if color == WHITE:
        if AttackMasks.pawn(sqr, BLACK)                   & piece_bitboards[P]: return True
        if AttackMasks.knight(sqr)                        & piece_bitboards[N]: return True
        if AttackMasks.king(sqr)                          & piece_bitboards[K]: return True
        if AttackMasks.rook(sqr, color_bitboards[BOTH])   & piece_bitboards[R]: return True
        if AttackMasks.bishop(sqr, color_bitboards[BOTH]) & piece_bitboards[B]: return True
        if AttackMasks.queen(sqr, color_bitboards[BOTH])  & piece_bitboards[Q]: return True
    return False


# About 10x faster than normal mask generator
class AttackMasks:
    @classmethod
    def pawn(cls, sqr, color):
        """..."""
        return PAWN_ATTACK_MASKS[color][sqr]
    
    @classmethod
    def knight(cls, sqr):
        """..."""
        return KNIGHT_ATTACK_MASKS[sqr]
    
    @classmethod
    def king(cls, sqr):
        """..."""
        return KING_ATTACK_MASKS[sqr]

    @classmethod
    def bishop(cls, sqr, block):
        """Return bishop lexical attack mask with regard to blockers."""
        occupancy = block & BISHOP_ATTACK_MASKS[sqr]
        return BISHOP_OCCUPANCY_ATTACK_MAP[sqr][occupancy]

    @classmethod
    def rook(cls, sqr, block):
        """..."""
        occupancy = block & ROOK_ATTACK_MASKS[sqr]
        return ROOK_OCCUPANCY_ATTACK_MAP[sqr][occupancy]

    @classmethod
    def queen(cls, sqr, block):
        """..."""
        return cls.bishop(sqr, block) | cls.rook(sqr, block)



# Deprecated. This is used to create attack mask lookups.
class AttackMasksComputed:
    def pawn(sqr, color):
        """compute a mask for the squares attacked by a pawn of color c and at position sqr"""
        assert 0 <= sqr <= 63
        assert color in [BLACK, WHITE]  # NOTE validation may lower perormance, consider moving outside of function!
        position = bop.mask_bit(sqr)
        attack = EMPTY
        if color == BLACK: attack = position << 7 | position << 9
        if color == WHITE: attack = position >> 7 | position >> 9
        if sqr%8 == A_FILE: attack &= EMPTY_GH # Edge cases... 
        if sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
        attack &= FULL # truncate overhang
        return attack

    def knight(sqr):
        """compute a mask for the squares attacked by a knight at position sqr"""
        assert 0 <= sqr <= 63
        position = bop.mask_bit(sqr)
        attack  = position << 6 | position << 10 | position << 15 | position << 17
        attack |= position >> 6 | position >> 10 | position >> 15 | position >> 17
        if sqr%8 == A_FILE or sqr%8 == B_FILE: attack &= EMPTY_GH # Edge cases... 
        if sqr%8 == G_FILE or sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
        attack &= FULL # truncate overhang
        return attack

    def king(sqr):
        """compute a mask for the squares attacked by a king at position sqr"""
        assert 0 <= sqr <= 63
        position = bop.mask_bit(sqr)
        attack  = position << 1 | position << 7 | position << 8 | position << 9
        attack |= position >> 1 | position >> 7 | position >> 8 | position >> 9
        if sqr%8 == A_FILE: attack &= EMPTY_GH # Edge cases... 
        if sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
        attack &= FULL # truncate overhang
        return attack

    # SLIDING PIECES
    def bishop(sqr, block):
        """compute a mask for the squares attacked by a bishop at position sqr"""
        assert 0 <= sqr <= 63
        attack = EMPTY

        MAX, MIN = 7, 0 # set to 6, 1 to exclude edges

        rank, file = sqr//8, sqr%8
        while rank < MAX and file < MAX: # down right
            rank += 1
            file += 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break # break if obstructing piece
        rank, file = sqr//8, sqr%8
        while rank > MIN and file < MAX: # up right
            rank -= 1
            file += 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        rank, file = sqr//8, sqr%8
        while rank < MAX and file > MIN: # down left
            rank += 1
            file -= 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        rank, file = sqr//8, sqr%8
        while rank > MIN and file > MIN: # up left
            rank -= 1
            file -= 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        return attack

    def rook(sqr, block): 
        """compute a mask for the squares attacked by a rook at position sqr"""
        assert 0 <= sqr <= 63
        attack = EMPTY

        MAX, MIN = 7, 0 # set to 6, 1 to exclude edges
        
        rank, file = sqr//8, sqr%8
        while rank < MAX: # up
            rank += 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break # break if obstructing piece
        rank = sqr//8
        while rank > MIN: # down
            rank -= 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        rank = sqr//8
        while file < MAX: # right
            file += 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        file = sqr%8
        while file > MIN: # left
            file -= 1
            attack |= 0b1 << rank*8+file
            if (block & 0b1 << rank*8+file): break
        return attack

    @classmethod
    def queen(cls, sqr, block):
        """compute a mask for the squares attacked by a rook at position sqr"""
        assert 0 <= sqr <= 63
        attack = cls.bishop(sqr, block) | cls.rook(sqr, block)
        return attack
