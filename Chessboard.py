

# Definitions
empty_square = "-"

# Imports
from ChessPiece import ChessPiece
from ChessRules import ChessRules



class Chessboard:
    def __init__(self):
        self.FEN = "rhbqkbhr/pppppppp/--------/--------/--------/-----h--/PPPPPPPP/RHBQKBHR"
        
        self.board = [[empty_square for _ in range(8)] for _ in range(8)]
        

        self.moves = 0

        self.ctmm = ['w', 'b'][self.moves%2]

        self.castling_rights = [["q", "k"], ["Q", "K"]]
        
        self.pieces_on_board = []



    # TERMINAL METHODS

    def print_board(self):
        """Prints a simple representation of the board in the terminal"""
        for i in range(8):
            print(8-i, end="    ")
            for j in range(8):
                if self.board[i][j] is empty_square:
                    print("-", end=" ")
                else:
                    print(self.board[i][j].char, end=" ")
            print()
        print("\n     ", end="")
        for i in range(8):
            print(chr(i+65), end=" ")
        print()
        print(f"ctmm: {self.ctmm}")


    def print_all_legal_moves(self):
        """Prints the legal moves of each piece"""
        for piece in self.pieces_on_board:
            print(piece.char, piece.legal_moves)   


    def illustrate_move(self, from_square, to_square):
        """Moves a piece to a square granted the move is legal"""
        # Converts chess coordinate to matrix index
        from_coord = f"{8-int(from_square[1])}{ord(from_square[0].upper())-65}"
        to_coord = f"{8-int(to_square[1])}{ord(to_square[0].upper())-65}"
        i1, j1 = int(from_coord[0]), int(from_coord[1])
        i2, j2 = int(to_coord[0]), int(to_coord[1])
        
        move = ChessRules(self, from_coord, to_coord)
        if move.legality is True:
            # Relocates and removes pieces, updates piece current position
            if self.board[i2][j2] is not empty_square:
                target_piece = self.board[i2][j2]
                self.pieces_on_board.remove(target_piece)

            self.board[i2][j2] = move.moving_piece
            self.board[i1][j1] = empty_square

            move.moving_piece.position = to_coord
            self.update_legal_moves()

            self.moves += 1
            self.ctmm = ['w', 'b'][self.moves%2]
            print(f"{from_coord} to {to_coord} was successful")
        
        # Reprint board and pieces' moves
        # self.print_all_legal_moves()
        self.print_board()


    def move_asker(self):
        while True:
            move = str(input("move piece [from-to] : "))
            from_square = move[:2]
            to_square = move[2:4]
            self.illustrate_move(from_square, to_square)



    # MAIN METHODS

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


    def update_legal_moves(self):
        """Updates legal moves for remaining pieces according to board state"""
        for piece in self.pieces_on_board:
            piece.assign_legal_moves(self.board)

          








# Program execution

board = Chessboard()
board.set_up_pieces()
board.give_pieces_consciousness()
# board.print_all_legal_moves()
board.print_board()
board.move_asker()






""" Sketch

8   00 01 02 03 04 05 06 07
7   10 11 12 13 14 15 16 17
6   20 21 22 23 24 25 26 27
5   30 31 32 33 34 35 36 37
4   40 41 42 43 44 45 46 47
3   50 51 52 53 54 55 56 57
2   60 61 62 63 64 65 66 67
1   70 71 72 73 74 75 76 77

    A  B  C  D  E  F  G  H
"""
