

class Chessboard:
    def __init__(self):
        self.FEN = "rhbqkbhr/--------/--------/--------/--------/RHBQKBHR"
        self.board = [[0 for _ in range(8)] for _ in range(8)]
        self.ctmm = "w"
        self.castling_rights = [["q", "k"], ["Q", "K"]]