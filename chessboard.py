


class Chessboard:
    def __init__(self):
        self.FEN = "rhbqkbhr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RHBQKBHR"
        self.fifty_move_rule = 0
        self.ctmm = "w"
        self.en_passent = None
        self.castle = [["b", "k"], ["Q", "K"]]
        self.board = [["*" for _ in range(8)] for _ in range(8)]


    # Terminal methods
    def print_board(self):
        """Prints a simple board in the terminal"""
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
        """Adds chess pieces according to the start set up"""
        pass



Chessboard = Chessboard()
Chessboard.print_board()