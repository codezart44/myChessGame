from src.chess.lookup.bit_counts import BITCOUNT_LOOKUP_TABLE

# import BitOperations as bo
class BitOperations:
    @classmethod
    def toggle_bit(cls, bitboard, square):
        """toggle the bit at position n"""
        return bitboard ^ (0b1 << square) # XOR with masked bit

    @classmethod
    def mask_bit(cls, square):
        """return empty but with square masked"""
        # mask for bit to toggle
        return 0b1 << square

    @classmethod
    def set_bit(cls, bitboard, square):
        """set the bitboard square to 1"""
        return bitboard | (0b1 << square) # OR with masked bit

    @classmethod
    def set_bits(cls, bitboard, squares):
        """Set the bitboard squares to 1."""
        for square in squares:
            bitboard |= 0b1 << square
        return bitboard

    @classmethod
    def get_bit(cls, bitboard, square):
        """get value of bit at square from bitboard"""
        return (bitboard >> square) & 0b1

    @classmethod
    def zero_bit(cls, bitboard, square):
        """set bit at square to zero"""
        if bitboard & (0b1 << square) == 0b0:
            return bitboard
        return bitboard ^ (0b1 << square)

    @classmethod
    def count_bits8(cls, bitboard):  # About x5 times faster than count_bits64!
        """count the number of active bits in board bit for byte"""
        counter = 0
        while bitboard:
            counter += BITCOUNT_LOOKUP_TABLE[bitboard & 0b11111111]
            bitboard >>= 8
        return counter

    @classmethod
    def lsb_index(cls, bitboard):
        """Retrieve the index of the least significant bit (LSB)"""
        if bitboard == 0b0: return -1
        return cls.count_bits8((bitboard & -bitboard) - 0b1) # count bits prior to lsb, same as lsb index
    
    @classmethod
    def is_zero_at(cls, bitboard, square):
        """Check if bitboard is zero at specified square."""
        return (bitboard & (0b1 << square)) == 0b0
