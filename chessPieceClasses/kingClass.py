
import numpy as np
from chessPieceClasses.baseClass import ChessPiece





class King(ChessPiece):
    def __init__(self, i, j, char) -> None:
        super().__init__(i, j, char)
        self.char = char
        self.color = 'w' if char.isupper() else 'b'
        pass

      
    def attacking_squares(self, matrix):
        '''
        return a list of all squares this bishop is attacking
        '''
        squares = []
        moves = [
            (-1, -1), (-1, 1), (1, -1), (1, 1),
            (-1, 0), (0, 1), (1, 0), (0, -1)
            ]
        for m in moves:
            i2 = self.i + m[0]
            j2 = self.j + m[1]

            if not 0 <= i2 <= 7 or not 0 <= j2 <= 7:
                continue
        
            target = matrix[i2, j2]
            if target != 0:
                if self.color != target.color:
                    squares.append((i2, j2))
                    continue
                if self.color == target.color:
                    continue
            squares.append((i2, j2))

        return squares


    def __validate_castle(self, i2, j2, matrix):

        assert self.times_moved == 0, 'King has already moved and lost the rights to castle'
        assert self.j == 4, 'King has already moved and lost the rights to castle'
        

        # find rooks, assert they haven't moved
        # alt. use castling rights in board_class to decide

        'R O-O-O K'
        # Squares to the left of the given king
        R1 = (self.i, self.j-4)
        O1 = (self.i, self.j-3)
        O2 = (self.i, self.j-2)
        O3 = (self.i, self.j-1)

        if (i2, j2) in [R1, O1, O2]:
            
            for O in [O2, O3, (self.i, self.j)]:
                i, j = O[0], O[1]
                assert not self.pieces_attacking_square(i, j, matrix), 'Cannot caslte through attacked squares'

            for O in [O1, O2, O3]:
                i, j = O[0], O[1]
                assert matrix[i, j] == 0, 'Cannot castle when pieces between king and rook are obstructing'
            
            # left rook
            R1 = matrix[self.i, self.j-4]
            if R1:                                                      # not 0
                assert R1.char.lower() == 'r'
                assert R1.times_moved == 0
                assert R1.i == self.i and R1.j == 0


        'K O-O R'
        O4 = (self.i, self.j+1)
        O5 = (self.i, self.j+2)
        R2 = (self.i, self.j+3)

        if (i2, j2) in [O5, R2]:

            for O in [(self.i, self.j), O4, O5]:
                i, j = O[0], O[1]
                assert not self.pieces_attacking_square(i, j, matrix), 'Cannot caslte through attacked squares'

            for O in [O4, O5]:
                i, j = O[0], O[1]
                assert matrix[i, j] == 0, 'Cannot castle when pieces between king and rook are obstructing'

            # right rook
            R2 = matrix[self.i, self.j+3]
            if R2:
                print(R2)
                assert R2.char.lower() == 'r'
                assert R2.times_moved == 0
                assert R2.i == self.i and R2.j == 7



    def __validate_king_move(self, i2, j2, matrix):
        '''
        if making a basic king move by one square
        '''
        self.validate_basics(i2, j2, matrix)            # will always be validated, unconditionally
        assert (i2, j2) in self.attacking_squares(matrix), 'The king isn\'t attacking that square'


    def validator(self, i2, j2, matrix):
        '''
        
        '''
        if self.times_moved == 0 and i2 == self.i and np.abs(j2-self.j) > 1:
            self.__validate_castle(i2, j2, matrix)
            self.absolute_castle(i2, j2, matrix)
        else:
            self.__validate_king_move(i2, j2, matrix)
            self.absolute_move(i2, j2, matrix)
        







""" Sketch

00 01 02 03 04 05 06 07
10 11 12 13 14 15 16 17
20 21 22 23 24 25 26 27
30 31 32 33 34 35 36 37
40 41 42 43 44 45 46 47
50 51 52 53 54 55 56 57
60 61 62 63 64 65 66 67
70 71 72 73 74 75 76 77

"""