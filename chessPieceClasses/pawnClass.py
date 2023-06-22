
import numpy as np
from chessPieceClasses.baseClass import ChessPiece
from chessPieceClasses.queenClass import Queen




class Pawn(ChessPiece):
    def __init__(self, i, j, char) -> None:
        super().__init__(i, j, char)
    
        self.last_move_double = False                   # used to track which pawns can be captured with en passent

        
    
    def attacking_squares(self, matrix):
        attacked = []
        if self.color == 'w':
            moves = [(-1, -1), (-1, 1)]
        if self.color == 'b':
            moves = [(1, 1), (1, -1)]

        for m in moves:
            i2, j2 = self.i, self.j
            i2 += m[0]
            j2 += m[1]

            if not 0 <= i2 <= 7 or not 0 <= j2 <= 7:
                continue
        
            target = matrix[i2, j2]
            if target == 0:
                continue
            if self.color == target.color:
                continue
            if self.color != target.color:
                attacked.append((i2, j2))
                continue
            
        return attacked
    
    

    def validate_pawn_move(self, i2, j2, matrix):
        '''
        
        '''
        self.validate_basics(i2, j2, matrix)
        assert j2 == self.j, 'Pawns may not move to other files, except for captures'


        if self.color == 'w':
            assert i2 in [self.i-1, self.i-2], 'Pawns may only move one or two steps forward'

            squares_in_front = [matrix[self.i-1, self.j], matrix[self.i-2, self.j]]

            if i2 == self.i-1:
                assert not np.any(squares_in_front[0]), 'Pawns cannot capture orthogonally'
            if i2 == self.i-2:
                assert self.times_moved == 0, 'Pawn has already moved, cannot be pushed'
                assert not np.any(squares_in_front), 'Pawns cannot capture orthogonally'
                self.last_move_double = True
            

        if self.color == 'b':
            assert i2 in [self.i+1, self.i+2]

            squares_in_front = [matrix[self.i+1, self.j], matrix[self.i+2, self.j]]

            if i2 == self.i+1:
                assert not np.any(squares_in_front[0]), 'Pawns cannot capture orthogonally'
            if i2 == self.i+2:
                assert self.times_moved == 0, 'Pawn has already moved, cannot be pushed'
                assert not np.any(squares_in_front), 'Pawns cannot capture orthogonally'
                self.last_move_double =True


    

    def validate_pawn_capture(self, i2, j2, matrix):
        '''
        
        '''
        # build in en passant capture

        self.validate_basics(i2, j2, matrix)

        if not matrix[i2, j2]:                                                                          # NOTE if there is a target, capture is legal. No further logic required

            passing_pawn:Pawn = matrix[i2+1, j2] if self.color == 'w' else matrix[i2-1, j2]      # passing pawn on same rank as attacking pawn

            assert passing_pawn and passing_pawn.color != self.color, 'No enemy pawn to capture'
            assert passing_pawn.last_move_double, 'Only pawns pushed on the prior move can be captured through en passant'

            if self.color == 'w':
                matrix[i2+1, j2] = 0
            if self.color == 'b':
                matrix[i2-1, j2] = 0

        else:
            assert (i2, j2) in self.attacking_squares(matrix), 'No piece to capture'


    def auto_queen_promotion(self, matrix):
        '''
        
        '''
        if self.color == 'w':
            if self.i == 0:
                matrix[self.i, self.j] = Queen(i=self.i, j=self.j, char='Q')
        if self.color == 'b':
            if self.i == 7:
                matrix[self.i, self.j] = Queen(i=self.i, j=self.j, char='q')



    def validator(self, i2, j2, matrix):
        '''
        
        '''
        ## Need to check move history for en passent

        if np.abs(j2-self.j) == 1:
            self.validate_pawn_capture(i2, j2, matrix)
            self.absolute_move(i2, j2, matrix)
        else:
            self.validate_pawn_move(i2, j2, matrix)
            self.absolute_move(i2, j2, matrix)

        self.auto_queen_promotion(matrix)


        ## promoting move
        # seudo: matrix[self.i, self.j] = queen
        # NOTE both captures and simple moves can lead to promotion ==> have outside function monitoring pawn reaching end of board











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