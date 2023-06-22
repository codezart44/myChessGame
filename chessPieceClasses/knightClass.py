
import numpy as np
from chessPieceClasses.baseClass import ChessPiece




class Knight(ChessPiece):
    def __init__(self, i, j, char) -> None:
        super().__init__(i, j, char)
        # self.movement_pattern = [12, 21, 19, 8, -12, -21, -19, -8]            # could be used for slighty faster computation 
        

    def attacking_squares(self, matrix):
        attacked = []
        moves = [
            (-2, 1), (-1, 2), (1, 2), (2, 1),
            (2, -1), (1, -2), (-1, -2), (-2, -1)
            ]
        for m in moves:
            i2, j2 = self.i, self.j
            i2 += m[0]
            j2 += m[1]

            if not 0 <= i2 <= 7 or not 0 <= j2 <= 7:
                continue
        
            target = matrix[i2, j2]
            if target != 0:
                if self.color != target.color:
                    attacked.append((i2, j2))
                    continue
                if self.color == target.color:
                    continue
            attacked.append((i2, j2))

        return attacked


    def validate_knight_jump(self, i2, j2, matrix):
        '''
        
        '''
        self.validate_basics(i2, j2, matrix)
        # from_index = int(f'{self.i}{self.j}')
        # to_index = int(f'{i2}{j2}')
        # dif = to_index - from_index
        # assert dif in self.movement_pattern
        assert (i2, j2) in self.attacking_squares(matrix), 'The knight may only jump in an L-shape'



    def validator(self, i2, j2, matrix):
        '''
        
        '''
        self.validate_knight_jump(i2, j2, matrix)
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