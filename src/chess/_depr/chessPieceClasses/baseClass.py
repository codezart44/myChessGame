
import numpy as np



class ChessPiece:
    def __init__(self, i, j, char:str) -> None:

        self.i, self.j = i, j

        self.char = char
        self.color = 'w' if char.isupper() else 'b'

        self.legal_moves = []
        self.times_moved = 0
    

    
    def absolute_move(self, i2, j2, matrix, ) -> None:
        '''
        
        '''
        piece:ChessPiece = matrix[self.i, self.j]
        matrix[i2, j2] = piece
        matrix[self.i, self.j] = 0

        piece.i, piece.j = i2, j2
        piece.times_moved += 1

        return matrix


    def absolute_castle(self, i2, j2, matrix):
        side = ''
        if j2 < self.j:
            side += 'queen'

            king:ChessPiece = matrix[self.i, self.j]
            rook:ChessPiece = matrix[self.i, 0]
            
            matrix[king.i, king.j] = 0
            matrix[rook.i, rook.j] = 0
            
            matrix[king.i, king.j-2] = king
            matrix[rook.i, rook.j+3] = rook

            king.j = king.j-2
            king.times_moved += 1
            rook.j = rook.j+3


        if j2 > self.j:
            side += 'king'

            king = matrix[self.i, self.j]
            rook = matrix[self.i, 7]
            
            matrix[king.i, king.j] = 0
            matrix[rook.i, rook.j] = 0
            
            matrix[king.i, king.j+2] = king
            matrix[rook.i, rook.j-2] = rook

            king.j = king.j+2
            king.times_moved += 1
            rook.j = rook.j-2

        print(f'{self.color} {side} side castle')
        

    def __validate_on_board(self, i2, j2) -> None:
        assert 0 <= i2 <= 7 and 0 <= j2 <= 7, 'Move is out of board'


    def __validate_legal_target(self, i2, j2, matrix) -> None:
        target = matrix[i2, j2]
        if target:
            assert target.color != self.color, 'Cannot attack or move to a friendly piece'


    def __validate_not_in_check(self, i2, j2, matrix:np.ndarray) -> None:
        '''
        
        '''
        i1, j1 = self.i, self.j                                                         # need orig coords to restore after ghost matrix absolute move

        ghost_matrix = matrix.copy()
        ghost_matrix = self.absolute_move(i2, j2, ghost_matrix)                         # make move on ghost board (the copy)

        pieces_on_board = ghost_matrix.ravel()[ghost_matrix.ravel()!=0]
        king = next(filter(lambda piece: piece.char.upper() == 'K' and piece.color == self.color, pieces_on_board))       # Locates friendly king
        checking_pieces = self.pieces_attacking_square(king.i, king.j, ghost_matrix)

        self.i, self.j = i1, j1
        self.times_moved -= 1

        assert not checking_pieces, 'Move will result in friendly king being in check'


    def validate_basics(self, i2, j2, matrix) -> None:
        self.__validate_on_board(i2, j2)
        self.__validate_legal_target(i2, j2, matrix)
        self.__validate_not_in_check(i2, j2, matrix)

    
    def pieces_attacking_square(self, i, j, matrix) -> list[object]:
        '''returns a list of all pieces attacking the square i, j'''

        pieces_on_board = matrix.ravel()[matrix.ravel()!=0]
        enemy_pieces = list(filter(lambda piece: piece.color != self.color, pieces_on_board))                                       # Finds all enemy pieces on board
        pieces = list(filter(lambda enemy_piece: (i, j) in enemy_piece.attacking_squares(matrix), enemy_pieces))                    # Filters pieces attacking a certain square
        
        return pieces





    # def validate_no_obstruction(f):
    #     def move_to(self, i2, j2, matrix):
            

    #         from_index = int(f'{self.i}{self.j}')
    #         to_index = int(f'{i2}{j2}')
    #         dif = to_index - from_index

    #         if 0 in (dif%9, dif%11):
    #             segment = matrix[min(self.i, i2)+1:max(self.i, i2), min(self.j, j2)+1:max(self.j, j2)]
    #             if dif%9 == 0:
    #                 segment = np.rot90(segment)
    #             sliding_path = np.diag(segment)
            
    #         elif i2 == self.i or j2 == self.j:
    #             if i2 == self.i:
    #                 sliding_path = matrix[self.i, min(self.j, j2)+1:max(self.j, j2)]
    #             if j2 == self.j:
    #                 sliding_path = matrix[min(self.i, i2)+1:max(self.i, i2), self.j]
            
    #         assert not any(sliding_path)

    #         print(sliding_path)
    #         f(self, i2, j2, matrix)

    #     return move_to


    
        # # target = matrix[i2, j2]
        # # i1, j1 = self.i, self.j

        # # matrix[i2, j2] = self
        # # matrix[self.i, self.j] = 0
        # # self.i, self.j = i2, j2


        # pieces_on_board = ghost_matrix.ravel()[ghost_matrix.ravel()!=0]
        # king = next(filter(lambda piece: piece.char.upper() == 'K' and piece.color == self.color, pieces_on_board))       # Locates friendly king
        # checking_pieces = self.attacking_pieces(king.i, king.j, ghost_matrix)
        
        # # matrix[i2, j2] = target
        # # matrix[i1, i1] = self
        # # self.i, self.j = i1, j1

        # assert len(checking_pieces) == 0



    
    





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
