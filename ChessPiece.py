
# DEFINITIONS
# Directions
empty_square = "-"
import numpy as np


class ChessPiece:
    """Supporting class for Chessboard"""
    def __init__(self, char, index):
        self.char = char
        self.index = index
        self.i, self.j = int(self.index[0]), int(self.index[1])


        # Uppercase - White & Lowercase - Black
        if char.isupper() is True:
            self.colour = "w"
        if char.islower() is True:
            self.colour = "b"

        
        self.fixed = False
        self.orthogonal = False
        self.diagonal = False

        if self.char.upper() in ["P", "H", "K"]:
            self.fixed = True
            self.get_fixed_moves()
        if self.char.upper() in ["R", "Q"]:
            self.orthogonal = True
        if self.char.upper() in ["B", "Q"]:
            self.diagonal = True

        self.legal_moves = []

        self.times_moved = 0



    # Initial methods

    def get_fixed_moves(self):
        """Assigns values representing the change of index for piece specific moves"""
        # Non sliding pieces
        if self.char == "p":
            self.movement_pattern = [10, 20]
        if self.char == "P":
            self.movement_pattern = [-10, -20]
        if self.char.upper() == "H":
            self.movement_pattern = [12, 21, 19, 8, -12, -21, -19, -8]
        if self.char.upper() == "K":
            self.movement_pattern = [-10, -9, 1, 11, 10, 9, -1, -11]
 


    # Callable methods
    def move_to(self, index, board):
        index_diff = int(index) - int(self.index)
        i2, j2 = int(index[0]), int(index[1])

        if self.move_within_board(index) and index_diff != 0:
            target = board.board[i2, j2]

            if self.fixed:
                if index_diff in self.movement_pattern:
                    if target == empty_square or self.colour != target.colour:
                        return True
                return False

            if self.orthogonal:
                if i2 == self.i or j2 == self.j:
                    if i2 == self.i:
                        orthogonal = board.board[self.i, min(self.j, j2):max(self.j, j2)+1]
                    if j2 == self.j:
                        orthogonal = board.board[min(self.i, i2):max(self.i, i2)+1, self.j]
                    if all([True if square in [empty_square, self, target] else False for square in orthogonal]):     # if all sqaures in board_segement are empty squares
                        if target == empty_square or self.colour != target.colour:
                            return True
                        return False

            if self.diagonal:
                if 0 in [index_diff%9, index_diff%11]:
                    matrix_segment = board.board[min(self.i, i2):max(self.i, i2)+1, min(self.j, j2):max(self.j, j2)+1]
                    if index_diff%9 == 0:                       # if moving diagonally up to the right we need to rotate matrix 90 deg.
                        matrix_segment = np.rot90(matrix_segment)
                    diagonal = np.diag(matrix_segment)
                    if all([True if square in [empty_square, self, target] else False for square in diagonal]):
                        if target == empty_square or self.colour != target.colour:
                            return True
                        return False
        return False


    def __str__(self):
        """In case of printing piece"""
        return self.char


    # Sub methods

    def move_within_board(self, index):
        """Checks whether a given square index is on the board"""
        if int(index) in range(78):
            i = int(index[0])
            j = int(index[1])
            if i in range(8) and j in range(8):
                return True
        return False







        
    



# piece = ChessPiece("Q", "h8")
# piece.give_move_vals()
# piece.give_sliding_moves("board")
# print(piece.legal_moves)





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



# OLD

    # def assign_legal_moves(self, board):
    #     """Master move assignement function"""
    #     self.legal_moves = []

    #     if self.sliding is False:
    #         self.give_fixed_moves(board)
    #     if self.sliding is True:
    #         self.give_sliding_moves(board)
            

    # def give_fixed_moves(self, board):
    #     """Assigns moves to pieces with fixed movement patterns"""
    #     for val in self.movement_pattern:
    #         move = str(int(self.index)+val)
    #         if len(move) == 1:
    #             move = f"0{move}"
    #         if self.move_within_board(move):
    #             i, j = int(move[0]), int(move[1])
    #             target = board[i][j]
    #             if target is empty_square:
    #                 self.legal_moves.append(move)
    #             elif self.colour is not target.colour:
    #                 self.legal_moves.append(move)


    # def give_sliding_moves(self, board):
    #     """Assigns moves to sliding pieces"""
    #     for direction in self.movement_pattern:
    #         for i in range(1, 8):
    #             move = str(int(self.index)+i*direction)
    #             if len(move) == 1:
    #                 move = f"0{move}"
    #             if self.move_within_board(move):
    #                 i, j = int(move[0]), int(move[1])
    #                 target = board[i][j]
    #                 if target is empty_square:
    #                     self.legal_moves.append(move)
    #                     continue
    #                 elif self.colour is not target.colour:
    #                     self.legal_moves.append(move)
    #                 break
    #             break

    

        # # Assigns sliding property
        # if self.char.upper() in ["P", "H", "K"]:
        #     self.sliding = False
        # if self.char.upper() in ["R", "B", "Q"]:
        #     self.sliding = True


        # N, E, S, W, NE, SE, SW, NW = -10, 1, 10, -1, -9, 11, 9, -11
           # # Sliding pieces
        # if self.char.upper() == "R":
        #     self.movement_pattern = [N, E, S, W]
        # if self.char.upper() == "B":
        #     self.movement_pattern = [NE, SE, SW, NW]
        # if self.char.upper() == "Q":
        #     self.movement_pattern = [N, E, S, W, NE, SE, SW, NW]