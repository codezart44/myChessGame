import random
from src.chess.bitboard.bits import BitOperations as bop
from src.chess.bitboard.attacks import AttackMasks as masks
from src.chess.bitboard.constants import *
from src.chess.lookup.attack_masks import (
    ROOK_ATTACK_MASKS,
    BISHOP_ATTACK_MASKS,
    ROOK_ATTACK_MASK_COUNTS,
    BISHOP_ATTACK_MASK_COUNTS,
    )

def get_blocking_configurations(index, mask_bit_count, attack_mask):
    """generate all possible occupancies of blocking pieces for sliding piece. """
    assert index >= 0, "Index must be non negative"
    assert index <= 2**mask_bit_count-1, "Index must be within upper bound of possible combinations"
    occupancy = EMPTY   
    for count in range(mask_bit_count):
        square = bop.lsb_index(attack_mask) # going through all masked bits in attack mask
        if (index & (0b1 << count)): # maps the binary string of index onto the rook attacking pattern. 
            occupancy |= (0b1 << square) # ORs with 1 leftshifted to align lsb
        attack_mask &= bop.zero_bit(attack_mask, square) # zeroing them out to find the next one next iteration
    # essentially maps the index number (bit string) to the the squares sliding piece can pass
    return occupancy

def generate_blocking_attack_map(piece_type):
    """Generate a mapping for all squares and possible occupancy configurations to the correct attack pattern. """
    # covering all occupancy attack mappings - replacing magic number (investigate later again)
    assert piece_type in [ROOK, BISHOP], "Only rook and bishop requires occupancy attack maps."
    blocking_attack_map = []
    for square in range(64):
        if piece_type == ROOK:
            attack_mask = ROOK_ATTACK_MASKS[square]
        if piece_type == BISHOP:
            attack_mask = BISHOP_ATTACK_MASKS[square]

        bit_count = bop.count_bits8(attack_mask)
        occup_count = 0b1 << bit_count # num possible occupancy configurations
        attacks = {} # stored attack patterns, indexed by occupancy configuration

        for index in range(occup_count): # populate occupancies and attacks
            occupancy = get_blocking_configurations(index, bit_count, attack_mask)
            if piece_type == ROOK:
                attacks[occupancy] = masks.rook(square, occupancy) # maps occupancy to attack
            if piece_type == BISHOP:
                attacks[occupancy] = masks.bishop(square, occupancy) # -//-
        
        blocking_attack_map.append(attacks) # add map for each square

    return blocking_attack_map # list of dicts




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

        if (bop.count_bits8(attack_mask * magic_number & 0x0000_0000_0000_00FF) > 6): continue

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
        occupancies[index] = get_blocking_configurations(index, bit_count, attack_mask) # store occupancy pattern
        if piece_type == ROOK:
            attacks[index] = masks.rook(square, occupancies[index])
        if piece_type == BISHOP:
            attacks[index] = masks.bishop(square, occupancies[index]) # store legal moves for occupancy pattern

    # start brute force testing random numbers as candidates for the "magic number"
    magic_number, magic_attack_map = scan_for_magic(occupancies, attacks, bit_count, attack_mask)
    if magic_number is not None:
        print(magic_number, (len(magic_attack_map) - magic_attack_map.count(0))/len(magic_attack_map))
    else:
        print('Failed to generate magic number, try to increase MAX_TRIES or threshold for num_magic_indices')
    
    return magic_number, magic_attack_map
