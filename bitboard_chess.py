import numpy as np
import random
from time import time
import json
from constants.attack_masks import *
from constants.notation import *    # main import from notation.py
from constants.bitcounts import *
from constants.attack_maps import BISHOP_OCCUPANCY_ATTACK_MAP, ROOK_OCCUPANCY_ATTACK_MAP # [square][occupancy]


# credit to: https://www.youtube.com/watch?v=0F_aeUik91A&list=PLmN0neTso3Jxh8ZIylk74JpwfiWNI76Cs&index=9

# Bitboard Chess
# 64 bit numbers






#=================================#
#         MAGIC BITBOARDS         #
#=================================#

def get_occupancy(index, mask_bit_count, attack_mask):
    """generate all possible occupancies of blocking pieces for sliding piece. """
    assert index >= 0, "Index must be non negative"
    assert index <= 2**mask_bit_count-1, "Index must be within upper bound of possible combinations"
    occupancy = EMPTY   
    for count in range(mask_bit_count):
        square = lsb_index(attack_mask) # going through all masked bits in attack mask
        if (index & (0b1 << count)): # maps the binary string of index onto the rook attacking pattern. 
            occupancy |= (0b1 << square) # ORs with 1 leftshifted to align lsb
        attack_mask &= zero_bit(attack_mask, square) # zeroing them out to find the next one next iteration
    # essentially maps the index number (bit string) to the the squares sliding piece can pass
    return occupancy

def magic_number_candidate():
    random_board = FULL
    for _ in range(3):
        random_board &= random.getrandbits(64)
    return random_board 

def scan_for_magic(occupancies, attacks, bit_count, attack_mask):
    NUM_TRIES = 100_000
    magic_maps_found = {}

    for _ in range(NUM_TRIES):
        magic_number = magic_number_candidate()

        if (count_bits8(attack_mask * magic_number & 0x0000_0000_0000_00FF) > 6): continue

        magic_attack_map = [0] * len(occupancies)
        fail = False

        for index in range(len(occupancies)): # scan for collisions for all possible occupancies
            occupancy, attack = occupancies[index], attacks[index] # get the occupancy configuration and corresponding attack mask
            magic_index = (occupancy * magic_number & FULL) >> (64-bit_count) # mask bit count being the number of relevant bits

            if magic_attack_map[magic_index] == 0: # no collision
                magic_attack_map[magic_index] = attack
            elif magic_attack_map[magic_index] != attack: # collision, magic index already used for another attack pattern
                fail = True
                break # try again

        # num_magic_indicies = len(magic_attack_map) - magic_attack_map.count(0) # num unique magic indicies used
        # if num_magic_indicies > 0b1 << (bit_count-1): # should at least half the occupancy count
        #     fail = True

        if fail == False:
            magic_maps_found[magic_number] = magic_attack_map
            # print('Num magic indicies:', num_magic_indicies, 'vs:', len(occupancies), 'ratio:', num_magic_indicies/len(occupancies))

    best_magic = min(magic_maps_found.keys())
    return (best_magic, magic_maps_found[best_magic])

def generate_magic_number(square, piece_type):
    """Generate magic number for mapping between occupancies and attack masks. """
    if piece_type == ROOK:
        attack_mask = ROOK_ATTACK_MASKS[square]
        bit_count = ROOK_ATTACK_MASK_COUNTS[square]
    if piece_type == BISHOP:
        attack_mask = BISHOP_ATTACK_MASKS[square]
        bit_count = BISHOP_ATTACK_MASK_COUNTS[square]

    assert bit_count <= 12 # maximum for rook in corner square, 12 possible blocking squares
    occup_count = 0b1 << bit_count # the number of possible occupancy pattern permutations, at most 2^12 = 4096
    occupancies = [0] * occup_count # current occupancy configuration
    attacks = [0] * occup_count # legal moves depending on occupancy configuration

    # populate occupancy patterns and corresponding attack patterns depending on the current occupancy
    for index in range(occup_count):
        occupancies[index] = get_occupancy(index, bit_count, attack_mask) # store occupancy pattern
        if piece_type == ROOK:
            attacks[index] = mask_rook_attack(square, occupancies[index])
        if piece_type == BISHOP:
            attacks[index] = mask_bishop_attack(square, occupancies[index]) # store legal moves for occupancy pattern

    # start brute force testing random numbers as candidates for the "magic number"
    magic_number, magic_attack_map = scan_for_magic(occupancies, attacks, bit_count, attack_mask)
    if magic_number is not None:
        print(magic_number, (len(magic_attack_map) - magic_attack_map.count(0))/len(magic_attack_map))
    else:
        print('Failed to generate magic number, try to increase MAX_TRIES or threshold for num_magic_indices')
    
    return magic_number, magic_attack_map

def generate_occupancy_attack_map(piece_type):
    """Generate a mapping for all squares and possible occupancy configurations to the correct attack pattern. """
    # covering all occupancy attack mappings - replacing magic number (investigate later again)
    occupancy_attack_map = []
    for square in range(64):
        if piece_type == ROOK:
            attack_mask = ROOK_ATTACK_MASKS[square]
        if piece_type == BISHOP:
            attack_mask = BISHOP_ATTACK_MASKS[square]

        bit_count = count_bits8(attack_mask)
        occup_count = 0b1 << bit_count # num possible occupancy configurations
        attacks = {} # stored attack patterns, indexed by occupancy configuration

        for index in range(occup_count): # populate occupancies and attacks
            occupancy = get_occupancy(index, bit_count, attack_mask)
            if piece_type == ROOK:
                attacks[occupancy] = mask_rook_attack(square, occupancy) # maps occupancy to attack
            if piece_type == BISHOP:
                attacks[occupancy] = mask_bishop_attack(square, occupancy) # -//-
        
        occupancy_attack_map.append(attacks) # add map for each square

    return occupancy_attack_map # list of dicts

#===============================#
#         PIECE ATTACKS         #
#===============================#

def index_to_coord(index):
    """Compute board square coordinate from board square index"""
    i = index//8
    j = index%8
    rank = 8-i
    file = chr(j+65)
    return f"{file}{rank}"

# LEAPER PIECES

def mask_pawn_attack(sqr, color):
    """compute a mask for the squares attacked by a pawn of color c and at position sqr"""
    assert 0 <= sqr <= 63
    assert color in [BLACK, WHITE]  # NOTE validation may lower perormance, consider moving outside of function!
    position = mask_bit(sqr)
    attack = EMPTY
    if color == BLACK: attack = position << 7 | position << 9
    if color == WHITE: attack = position >> 7 | position >> 9
    if sqr%8 == A_FILE: attack &= EMPTY_GH # Edge cases... 
    if sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
    attack &= FULL # truncate overhang
    return attack 

def mask_knight_attack(sqr):
    """compute a mask for the squares attacked by a knight at position sqr"""
    assert 0 <= sqr <= 63
    position = mask_bit(sqr)
    attack  = position << 6 | position << 10 | position << 15 | position << 17
    attack |= position >> 6 | position >> 10 | position >> 15 | position >> 17
    if sqr%8 == A_FILE or sqr%8 == B_FILE: attack &= EMPTY_GH # Edge cases... 
    if sqr%8 == G_FILE or sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
    attack &= FULL # truncate overhang
    return attack

def mask_king_attack(sqr):
    """compute a mask for the squares attacked by a king at position sqr"""
    assert 0 <= sqr <= 63
    position = mask_bit(sqr)
    attack  = position << 1 | position << 7 | position << 8 | position << 9
    attack |= position >> 1 | position >> 7 | position >> 8 | position >> 9
    if sqr%8 == A_FILE: attack &= EMPTY_GH # Edge cases... 
    if sqr%8 == H_FILE: attack &= EMPTY_AB # ...litterally
    attack &= FULL # truncate overhang
    return attack

# SLIDING PIECES

def mask_bishop_attack(sqr, block):
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

def mask_rook_attack(sqr, block): 
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

def mask_queen_attack(sqr, block):
    """compute a mask for the squares attacked by a rook at position sqr"""
    assert 0 <= sqr <= 63
    attack = mask_bishop_attack(sqr, block) | mask_rook_attack(sqr, block)
    return attack




"""
SEMANTIC REPRESENTATION
8    r  n  b  q  k  b  n  r
7    p  p  p  p  p  p  p  p
6    *  *  *  *  *  *  *  *
5    *  *  *  *  *  *  *  *
4    *  *  *  *  *  *  *  *
3    *  *  *  *  *  *  *  *
2    P  P  P  P  P  P  P  P
1    R  N  B  Q  K  B  N  R

     A  B  C  D  E  F  G  H

INDEX REPRESENTATION
8     0  1  2  3  4  5  6  7
7     8  9 10 11 12 13 14 15
6    16 17 18 19 20 21 22 23
5    24 25 26 27 28 29 30 31
4    32 33 34 35 36 37 38 39
3    40 41 42 43 44 45 46 47
2    48 49 50 51 52 53 54 55
1    56 57 58 59 60 61 62 63

     A  B  C  D  E  F  G  H
"""


#====================================#
#         BITBOARD FUNCTIONS         #
#====================================#

# board representation
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

# toggle bit
def toggle_bit(bitboard, square):
    """toggle the bit at position n"""
    return bitboard ^ (0b1 << square) # XOR with masked bit

# mask bit
def mask_bit(square):
    """return empty but with square masked"""
    # mask for bit to toggle
    return 0b1 << square

# set bit
def set_bit(bitboard, square):
    """set the bitboard square to 1"""
    return bitboard | (0b1 << square) # OR with masked bit

# get bit
def get_bit(bitboard, square):
    """get value of bit at square from bitboard"""
    return (bitboard >> square) & 0b1

# pop bit
def zero_bit(bitboard, square):
    """set bit at square to zero"""
    if bitboard & (0b1 << square) == 0b0:
        return bitboard
    return bitboard ^ (0b1 << square)

def count_bits8(bitboard):  # About x5 times faster than count_bits64!
    """count the number of active bits in board bit for byte"""
    counter = 0
    while bitboard:
        counter += BITCOUNT_LOOKUP_TABLE[bitboard & 0b11111111]
        bitboard >>= 8
    return counter

def lsb_index(bitboard):
    """Retrieve the index of the least significant bit (LSB)"""
    if bitboard == 0b0: raise ValueError("Empty bitboard (0b0) has no LSB")
    return count_bits8((bitboard & -bitboard) - 0b1) # count bits prior to lsb, same as lsb index


def main():
    occupancy = toggle_bit(EMPTY, F3)
    occupancy = toggle_bit(occupancy, F5)
    occupancy = toggle_bit(occupancy, C6)
    occupancy = toggle_bit(occupancy, C2)
    occupancy = toggle_bit(occupancy, G4)
    occupancy = toggle_bit(occupancy, E2)
    occupancy = toggle_bit(occupancy, E7)
    occupancy = toggle_bit(occupancy, D4)

    occupancy = zero_bit(occupancy, C5)
    print_bitboard(occupancy)

    square = D5





    # print('Reference')
    # rook_mask = mask_rook_attack(square, occupancy)
    # print_bitboard(rook_mask)

    # print('Magic occupancy')
    # magic_number, magic_attack_map = generate_magic_number(square, ROOK)

    # attack_mask = ROOK_ATTACK_MASKS[square]
    # bit_count = ROOK_ATTACK_MASK_COUNTS[square]
    
    # occupancy &= attack_mask
    # magic_index = (occupancy * magic_number & FULL) >> (64-bit_count)
    # attack = magic_attack_map[magic_index]
    # print_bitboard(attack)


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