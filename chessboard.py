



class Chessboard:
    def __init__(self):
        self.FEN = "rhbqkbhr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RHBQKBHR"
        self.fifty_move_rule = 0
        self.ctmm = "w"
        self.en_passent = None
        self.castle = [["q", "k"], ["Q", "K"]]
        self.board = [["*" for _ in range(8)] for _ in range(8)]


    # Terminal methods
    def print_board(self):
        """Prints a simple representation of the board in the terminal"""
        for i in range(8):
            print(8-i, end="    ")
            for j in range(8):
                print(self.board[i][j], end=" ")
            print()
        print("\n     ", end="")
        for i in range(8):
            print(chr(i+65), end=" ")


    # Main methods
    def set_up_pieces(self):
        """Places pieces on the board accoring to the FEN notation"""
        for i in range(8):
            for j in range(8):
                if self.FEN[9*i+j] != "/":
                    self.board[i][j] = self.FEN[9*i+j]
            




Chessboard = Chessboard()
Chessboard.set_up_pieces()
Chessboard.print_board()