

# Directions
N, E, S, W, NE, SE, SW, NW = -10, 1, 10, -1, -9, 11, 9, -11



class ChessPiece:
    def __init__(self, char, colour, coord):
        self.char = char
        self.colour = colour
        self.index = f"{8-int(coord[1])}{int(ord(coord[0].upper()))-65}"

        self.move_pattern = []

        self.legal_moves = []

        self.times_moved = 0


    def give_horse_moves(self):
        pass


    def give_set_moves(self):
        """For pieces with set moves"""

        if self.char.upper() == "H":
            self.move_pattern = [12, 21, 19, 8, -12, -21, -19, -8]

        if self.char.upper() == "K":
            self.move_pattern == [-10, 1, 10, -1, -9, 11, 9, -11]



    def give_sliding_moves(self):
        """For sliding pieces"""

        if self.char.upper() == "R":
            self.move_pattern = [N, E, S, W]

        if self.char.upper() == "B":
            self.move_pattern = [NE, SE, SW, NW]

        if self.char.upper() == "Q":
            self.move_pattern = [N, E, S, W, NE, SE, SW, NW]




piece = ChessPiece("Q", "b", "a8")
print(piece.index)





""" Sketch

00 01 02 03 04 05 06 07
10 11 12 13 14 15 16 17
20 21 22 23 24 25 26 27
30 31 32 33 34 35 36 37
40 41 42 43 44 45 46 47
50 51 52 53 54 55 56 57
60 61 62 63 64 65 66 67
70 71 72 73 74 75 76 77

8   o o o o o o o o
7   o o o o o o o o
6   o o o o o o o o
5   o o o o o o o o
4   o o o o o o o o
3   o o o o o o o o
2   o o o o o o o o
1   o o o o o o o o

    A B C D E F G H
"""