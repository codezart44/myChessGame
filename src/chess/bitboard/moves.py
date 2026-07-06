from src.chess.bitboard.constants import *
from src.chess.bitboard.bits import BitOperations as bop
from src.chess.bitboard.attacks import AttackMasks as masks
from src.chess.bitboard.utils import piece_to_color_bitboards, print_bitboard
from src.chess.bitboard.attacks import squared_attacked_by

# Seudo legal moves
# Moves are a subset of attacks
# A pinned piece will still attack its surrounding squares, it just cannot move there

def on_board(sqr) -> bool:
    """..."""
    return A8 <= sqr <= H1

def on_rank(sqr, rank) -> bool:
    """..."""
    return sqr // 8 == rank

def on_file(sqr, file) -> bool:
    """..."""
    return sqr % 8 == file

def get_bit_indicies(bitboard):
    """..."""
    indicies = []
    while bitboard > 0b0:
        tgt = bop.lsb_index(bitboard)
        indicies.append(tgt)
        bitboard = bop.zero_bit(bitboard, tgt)
    return indicies


def no_pieces_at(squares: list, bitboard) -> bool:
    """..."""
    clear = True
    for sqr in squares:
        clear = clear and bop.is_zero_at(bitboard, sqr)
    return clear

def no_attacks_at(squares: list, color, piece_bitboards, color_bitboards) -> bool:
    """..."""
    clear = True
    for sqr in squares:
        clear = clear and not squared_attacked_by(sqr, color, piece_bitboards, color_bitboards)
    return clear

# def puts_king_in_check(src, tgt, piece_bitboards, color_bitboards, color):


# pawn moves
# - push
# - double push
# - promote
# - capture
# - capture promote
# - en_passent
def pawn_moves(src, piece_bitboards, color_bitboards, color, enp_sqr):
    assert on_board(src)

    flags = {
        "push": False,
        "double push": False,
        "capture": False,
        "promote": False,
        "en passent": False,
    }
    moves = []

    is_white = (color == WHITE)
    assert piece_bitboards[P if is_white else p] & bop.mask_bit(src), "Bug. Should not fail."
    promotion_rank = RANK_8 if is_white else RANK_1
    start_rank = RANK_2 if is_white else RANK_7
    single_push = -8 if is_white else 8
    double_push = single_push * 2
    capture_left = -9 if is_white else 9
    capture_right = -7 if is_white else 7
    color_enemy = BLACK if is_white else WHITE

    # single push
    tgt = src + single_push
    if on_board(tgt) and bop.is_zero_at(color_bitboards[BOTH], tgt):
        moves.append(tgt)
        flags["push"] = True

        # push promote
        if on_rank(tgt, promotion_rank):
            flags["promote"] = True

    # double push
    tgt = src + double_push
    if (flags["push"] == True) and on_rank(src, start_rank) and bop.is_zero_at(color_bitboards[BOTH], tgt):
        moves.append(tgt)
        flags["double push"] = True
    
    # capture right
    if not on_file(src, A_FILE):
        tgt = src + capture_right
        if bop.mask_bit(tgt) & color_bitboards[color_enemy]:
            moves.append(tgt)
            flags["capture"] = True
            if on_rank(tgt, promotion_rank):
                # capture promote
                flags["promote"] = True
        if enp_sqr != NA and tgt == enp_sqr:
            # en passent
            moves.append(tgt)
            flags["en passent"] = True

    # capture left
    if not on_file(src, H_FILE):
        tgt = src + capture_left
        if bop.mask_bit(tgt) & color_bitboards[color_enemy]:
            moves.append(tgt)
            flags["capture"] = True
            if on_rank(tgt, promotion_rank):
                # capture promote
                flags["promote"] = True
        if enp_sqr != NA and tgt == enp_sqr:
            # en passent
            moves.append(tgt)
            flags["en passent"] = True
    
    return moves, flags

# king moves
# - leap
# - castle
def king_moves(src, piece_bitboards, color_bitboards, color, castle):
    assert on_board(src)
    is_white = (color == WHITE)
    assert bop.mask_bit(src) & piece_bitboards[K if is_white else k], "Bug. Should not fail."

    moves = []
    flags = {
        "leap": False,
        "castle king": False,
        "castle queen": False,
    }
    color_enemy = BLACK if is_white else WHITE

    # leaps
    leap_mask = masks.king(src) & ~color_bitboards[color]
    moves += get_bit_indicies(leap_mask)
    if len(moves) > 0: flags["leap"] = True

    # castling king side
    in_check = squared_attacked_by(src, color_enemy, piece_bitboards, color_bitboards)

    # castling queen side
    castle_q = castle & (WQ if is_white else BQ)
    if castle_q and not in_check:
        assert src == E1 if is_white else E8
        r1, r2, r3 = src-1, src-2, src-3
        no_pieces = no_pieces_at([r1, r2, r3], color_bitboards[BOTH])
        no_attacks = no_attacks_at([r1, r2, r3], color_enemy, piece_bitboards, color_bitboards)
        if (no_pieces and no_attacks):
            # allow castling queen-side
            moves.append(r3)
            flags["castle queen"] = True

    castle_k = castle & (WK if is_white else BK)
    if castle_k and not in_check:
        assert src == E1 if is_white else E8
        l1, l2 = src+1, src+2
        no_pieces = no_pieces_at([l1, l2], color_bitboards[BOTH])
        no_attacks = no_attacks_at([l1, l2], color_enemy, piece_bitboards, color_bitboards)
        if (no_pieces and no_attacks):
            # allow castling king-side
            moves.append(l2)
            flags["castle king"] = True

    return moves, flags

def knight_moves(src, piece_bitboards, color_bitboards, color):
    assert on_board(src)
    assert bop.mask_bit(src) & piece_bitboards[N if color == WHITE else n], "Bug. Should not fail."
    move_mask = masks.knight(src) & ~color_bitboards[color]
    return get_bit_indicies(move_mask)

def bishop_moves(src, piece_bitboards, color_bitboards, color):
    assert on_board(src)
    assert bop.mask_bit(src) & piece_bitboards[B if color == WHITE else b], "Bug. Should not fail."
    move_mask = masks.bishop(src, color_bitboards[BOTH]) & ~color_bitboards[color]
    return get_bit_indicies(move_mask)

def rook_moves(src, piece_bitboards, color_bitboards, color):
    assert on_board(src)
    assert bop.mask_bit(src) & piece_bitboards[R if color == WHITE else r], "Bug. Should not fail."
    move_mask = masks.rook(src, color_bitboards[BOTH]) & ~color_bitboards[color]
    return get_bit_indicies(move_mask)

def queen_moves(src, piece_bitboards, color_bitboards, color):
    assert on_board(src)
    assert bop.mask_bit(src) & piece_bitboards[Q if color == WHITE else q], "Bug. Should not fail."
    move_mask = masks.queen(src, color_bitboards[BOTH]) & ~color_bitboards[color]
    return get_bit_indicies(move_mask)


def get_moves(piece_bitboards, color_bitboards, color):
    is_white = color == WHITE
    pieces = WHITE_PIECES if is_white else BLACK_PIECES
    for piece in pieces:
        bitboard = piece_bitboards[piece]
        squares = get_bit_indicies(bitboard)
        for sqr in squares:
            if piece == (P if is_white else p):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in pawn_moves(sqr, piece_bitboards, color_bitboards, color, NA)[0]]
            if piece == (N if is_white else n):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in knight_moves(sqr, piece_bitboards, color_bitboards, color)]
            if piece == (B if is_white else b):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in bishop_moves(sqr, piece_bitboards, color_bitboards, color)]
            if piece == (R if is_white else r):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in rook_moves(sqr, piece_bitboards, color_bitboards, color)]
            if piece == (Q if is_white else q):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in queen_moves(sqr, piece_bitboards, color_bitboards, color)]
            if piece == (K if is_white else k):
                ASCII_PIECES[piece], INDEX_COORD_MAP[sqr], [INDEX_COORD_MAP[m] for m in king_moves(sqr, piece_bitboards, color_bitboards, color, 0b0000)[0]]






# Fully legal moves
# copy make instead of make reverse






