

import numpy as np
from chessPieceClasses.baseClass import ChessPiece




class Queen(ChessPiece):
    def __init__(self, i, j, char) -> None:
        super().__init__(i, j, char)

        
    
    def attacking_squares(self, matrix):
        attacked = []
        directions = [
            (-1, -1), (-1, 1), (1, -1), (1, 1),
            (-1, 0), (0, 1), (1, 0), (0, -1)
            ]
        for d in directions:
            i2, j2 = self.i, self.j

            while True:
                i2 += d[0]
                j2 += d[1]
                if not 0 <= i2 <= 7 or not 0 <= j2 <= 7:
                    break
            
                target = matrix[i2, j2]
                if target != 0:
                    if self.color != target.color:
                        attacked.append((i2, j2))
                        break
                    if self.color == target.color:
                        break
                attacked.append((i2, j2))

        return attacked
    

    def validate_queen_move(self, i2, j2, matrix):
        '''
        
        '''
        self.validate_basics(i2, j2, matrix)

        from_index = int(f'{self.i}{self.j}')
        to_index = int(f'{i2}{j2}')
        dif = to_index - from_index
        assert 0 in [dif%9, dif%11] or i2 == self.i or j2 == self.j, 'The queen may only move diagonally or orthogonally'

        assert (i2, j2) in self.attacking_squares(matrix), 'The queen is not attacking that square'




    def validator(self, i2, j2, matrix):
        '''
        
        '''
        self.validate_queen_move(i2, j2, matrix)
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
