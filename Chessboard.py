
from queue import Empty

# Definitions
empty = "-"


from calendar import c
from ChessPiece import ChessPiece


class Chessboard:
    def __init__(self):
        self.FEN = "rhbqkbhr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RHBQKBHR"
        
        self.board = [[empty for _ in range(8)] for _ in range(8)]
        
        self.ctmm = "w"
        
        self.castling_rights = [["q", "k"], ["Q", "K"]]
        
        self.pieces_on_board = []

    

    # Terminal methods

    def print_board(self):
        """Prints a simple representation of the board in the terminal"""
        for i in range(8):
            print(8-i, end="    ")
            for j in range(8):
                if self.board[i][j] == "-":
                    print("-", end=" ")
                else:
                    print(self.board[i][j].char, end=" ")
            print()
        print("\n     ", end="")
        for i in range(8):
            print(chr(i+65), end=" ")
        print()



    def print_all_legal_moves(self):
        """Prints the legal moves of each piece"""
        for piece in self.pieces_on_board:
            print(piece.legal_moves)   





    # Main methods

    def set_up_pieces(self):
        """Places piece objects on the board accorind to the FEN notation"""
        # Places piece objects on board
        for i in range(8):
            for j in range(8):
                if self.FEN[9*i+j] not in ["/", "-"]:
                    char = self.FEN[9*i+j]
                    index = f"{i}{j}"
                    piece = ChessPiece(char, index)
                    self.board[i][j] = piece
                    self.pieces_on_board.append(piece)



    def give_pieces_consciousness(self):
        """Assigns legal moves to all pieces with respect to surrounding pieces"""
        for piece in self.pieces_on_board:
            piece.assign_legal_moves(self.board)
        


          




    def make_move(self, from_square, to_square):
        pass


        





# Program execution
board = Chessboard()
board.set_up_pieces()
board.give_pieces_consciousness()
board.print_board()
board.print_all_legal_moves()








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
