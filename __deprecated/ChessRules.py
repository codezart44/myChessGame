

# Definitions
empty_square = "-"




class ChessRules:
    def __init__(self, chessboard, from_coord, to_coord):
        self.chessboard = chessboard
        self.board = chessboard.board
        self.from_coord = from_coord
        self.to_coord = to_coord
        self.i1, self.j1 = int(from_coord[0]), int(from_coord[1])
        self.i2, self.j2 = int(to_coord[0]), int(to_coord[1])

        self.ctmm = self.chessboard.ctmm

        self.moving_piece = self.board[self.i1][self.j1]
        self.target = self.board[self.i2][self.j2]
        

        # list of rules to be checked:
        rules = {
            self.basic_rules:'obstructed basic rule',
            self.not_in_check:'must move out of check'
        }
            
        

        """
        self.castling_rights,
        self.en_passent,
        self.50_move_rule
        """

        self.legality = True
        for i, rule in enumerate(rules):
            if rule() is False:
                self.legality = False
                print(f"{rules[rule]}")
        


    def basic_rules(self):
        """Fundamental rules of a legal chess move"""
        if self.moving_piece is empty_square:
            return False
        if self.moving_piece.color != self.ctmm:
            return False
        if self.to_coord not in self.moving_piece.legal_moves:
            return False
        return True



    def not_in_check(self):
        """A move cannot leave you in check; cannot put self in check and must escape check if king is in check"""
        self.make_move()
        opposite_color_pieces = list(filter(lambda piece: piece.color != self.ctmm, self.chessboard.pieces_on_board))                                       # Finds all enemy pieces on board
        king_position = next(filter(lambda piece: piece.char.upper() == 'K' and piece.color == self.ctmm, self.chessboard.pieces_on_board)).position        # Locates friendly king position
        checking_pieces = list(filter(lambda enemy_piece: king_position in enemy_piece.legal_moves, opposite_color_pieces))                                 # Extracts all pieces checking friendly king
        self.revert_move()

        if len(checking_pieces) != 0:
            return False
        return True


    ## NOTE should use .copy() on board to make ghost move and check legality on post move board state
    def make_move(self):
        """Temporarily makes the queued move to see whether in check or not after"""
        self.board[self.i2][self.j2] = self.moving_piece
        self.moving_piece.position = self.to_coord

        self.board[self.i1][self.j1] = empty_square
        if self.target in self.chessboard.pieces_on_board:
            self.chessboard.pieces_on_board.remove(self.target)
        self.chessboard.update_legal_moves()



    def revert_move(self):
        """Reverses temporary ghost move to pre move board state"""
        self.board[self.i1][self.j1] = self.moving_piece
        self.moving_piece.position = self.from_coord

        self.board[self.i2][self.j2] = self.target
        if self.target is not empty_square and self.target not in self.chessboard.pieces_on_board:
            self.chessboard.pieces_on_board.append(self.target)
        self.chessboard.update_legal_moves()









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
