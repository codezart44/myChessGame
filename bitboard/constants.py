# Bitboard Constants

# PIECE INDICIES 0-11
P,N,B,R,Q,K,p,n,b,r,q,k = range(12) # 

# PIECE DATA
ASCII_PIECES  =  "PNBRQKpnbrqk."
UNICODE_PIECES = "♟♞♝♜♛♚♙♘♗♖♕♔."

# BOARDS 
# Board read from right to left
# h8g8f8e8d8c8b8a8_h7g7f7e7d7c7b7a7_h6g6f6e6d6c6b6a6_h5g5f5e5d5c5b5a5_h4g4f4e4d4c4b4a4_h3g3f3e3d3c3b3a3_h2g2f2e2d2c2b2a2_h1g1f1e1d1c1b1a1
FULL  = 0b11111111_11111111_11111111_11111111_11111111_11111111_11111111_11111111
EMPTY = 0b00000000_00000000_00000000_00000000_00000000_00000000_00000000_00000000
EMPTY_AB = 0b11111100_11111100_11111100_11111100_11111100_11111100_11111100_11111100 # so knight moves dont wrap around (to remove from other side)
EMPTY_GH = 0b00111111_00111111_00111111_00111111_00111111_00111111_00111111_00111111 # -//-
TEST = 0b00100010_00011000_00001000_00000000_00100010_00000000_00010000_00000000

# FEN (Forsynth-Edward Notation) to describe chess board positions
# position : side : castling : en_passent :  full : half
EMPTY_FEN = '8/8/8/8/8/8/8/8 w - - 0 1'
START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
TRICKY_FEN = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1'

# SQUARES
A8,B8,C8,D8,E8,F8,G8,H8    =  0, 1, 2, 3, 4, 5, 6, 7
A7,B7,C7,D7,E7,F7,G7,H7    =  8, 9,10,11,12,13,14,15
A6,B6,C6,D6,E6,F6,G6,H6    = 16,17,18,19,20,21,22,23
A5,B5,C5,D5,E5,F5,G5,H5    = 24,25,26,27,28,29,30,31
A4,B4,C4,D4,E4,F4,G4,H4    = 32,33,34,35,36,37,38,39
A3,B3,C3,D3,E3,F3,G3,H3    = 40,41,42,43,44,45,46,47
A2,B2,C2,D2,E2,F2,G2,H2    = 48,49,50,51,52,53,54,55
A1,B1,C1,D1,E1,F1,G1,H1,NA = 56,57,58,59,60,61,62,63,-1

# FILES
A_FILE,B_FILE,C_FILE,D_FILE,E_FILE,F_FILE,G_FILE,H_FILE = 0,1,2,3,4,5,6,7

# COLORS
BLACK,WHITE,BOTH = 0,1,2

# SLIDING PIECES
ROOK,BISHOP = 0,1   # Queen is combination of both, not needed explicitly

# index to coord: INDEX_COORD_MAP[index]
# coord to index: INDEX_COORD_MAP.index(coord)
INDEX_COORD_MAP = [
    'A8','B8','C8','D8','E8','F8','G8','H8',
    'A7','B7','C7','D7','E7','F7','G7','H7',
    'A6','B6','C6','D6','E6','F6','G6','H6',
    'A5','B5','C5','D5','E5','F5','G5','H5',
    'A4','B4','C4','D4','E4','F4','G4','H4',
    'A3','B3','C3','D3','E3','F3','G3','H3',
    'A2','B2','C2','D2','E2','F2','G2','H2',
    'A1','B1','C1','D1','E1','F1','G1','H1', '-' # - For no square
]