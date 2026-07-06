from src.chess.bitboard.constants import *
from src.chess.bitboard.attacks import AttackMasks as masks
from src.chess.bitboard.bits import BitOperations as bop
from src.chess.bitboard.utils import print_bitboard, print_chessboard, fen_to_bitboards
from src.chess.bitboard.moves import pawn_moves, king_moves, knight_moves, bishop_moves, rook_moves, queen_moves, get_moves

# def print_squares_attacked_by(side, piece_bitboards, occup_bitboards):
#     print()
#     for i in range(8):
#         print(f'{8-i}   ', end='')
#         for j in range(8):
#             square = 8*i+j
#             print(f"{int(is_squared_attacked(square, side, piece_bitboards, occup_bitboards))}", end=" ")
#         print()
#     print('\n    A B C D E F G H\n')

# def move(f, t):
    # pass

def main():
    piece_bitboards, color_bitboards = fen_to_bitboards("r3k2r/p1ppqpb1/bn2pnp1/3PNK2/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1")
    print_bitboard(color_bitboards[BOTH])
    print_chessboard(piece_bitboards)
    # moves, flags = pawn_moves(G2, piece_bitboards, color_bitboards, WHITE, NA)
    # print([INDEX_COORD_MAP[m] for m in moves])
    # print(flags)

    # moves = king_moves(E1, piece_bitboards, color_bitboards, WHITE, CASTLING)
    # print([INDEX_COORD_MAP[m] for m in moves])

    # moves = knight_moves(, piece_bitboards, color_bitboards, BLACK)
    # print([INDEX_COORD_MAP[m] for m in moves])

    # moves = bishop_moves(G7, piece_bitboards, color_bitboards, BLACK)
    # print([INDEX_COORD_MAP[m] for m in moves])

    # moves = rook_moves(H8, piece_bitboards, color_bitboards, BLACK)
    # print([INDEX_COORD_MAP[m] for m in moves])

    # moves = queen_moves(F3, piece_bitboards, color_bitboards, WHITE)
    # print([INDEX_COORD_MAP[m] for m in moves])

    import time 
    start = time.time()
    for _ in range(100_000):
        get_moves(piece_bitboards, color_bitboards, WHITE)
    elapsed = time.time() - start
    print(elapsed / 100_000)
    # currently takes about 105 us (0.1ms) to find all possible pseudo legal moves for one color



if __name__=="__main__":
    main()



# credit to: https://www.youtube.com/watch?v=0F_aeUik91A&list=PLmN0neTso3Jxh8ZIylk74JpwfiWNI76Cs&index=9