

class ChessPiece:
    def __init__(self, char, colour, coord):
        self.char = char
        self.colour = colour
        self.index = f"{8-int(coord[1])}{int(ord(coord[0].upper())-65)}"

        self.move_pattern = []
        self.legal_moves = []
        self.times_moved = []







piece = ChessPiece("Q", "b", "e4")
print(piece.index)


