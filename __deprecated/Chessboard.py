
# Imports
from chessPieceClasses.kingClass import King
from chessPieceClasses.queenClass import Queen
from chessPieceClasses.rookClass import Rook
from chessPieceClasses.bishopClass import Bishop
from chessPieceClasses.knightClass import Knight
from chessPieceClasses.pawnClass import Pawn

import numpy as np
import traceback


class ChessGame:
    def __init__(self):

        self.FEN = "rnbqkbnr/pppppppp/--------/--------/--------/--------/PPPPPPPP/RNBQKBNR"
        # self.FEN = "-n--k-n-/pppppppp/--------/--------/--------/--------/PPPPPPPP/-N--K-N-"

        self.fancyFEN = '♖♘♗♕♔♗♘♖/♙♙♙♙♙♙♙♙/--------/--------/--------/--------/♟♟♟♟♟♟♟♟/♜♞♝♛♚♝♞♜'
        
        self.matrix = np.zeros([8, 8], dtype=object)

        self.active_color = 'w'                 # .
        self.castling_rights = 'KQkq'           # .
        self.en_passant = '-'                   # the square the pushed pawn passed, e.g. 'e3' after pushing a pawn to e4
        self.halfmove_clock = 0                 # ticks up when a non pawn piece is moved without capture
        self.fullmove_clock = 1                 # ticks up after black's move

        self.piece_dict = {'k': King, 'q': Queen, 'r': Rook, 'b': Bishop, 'n': Knight, 'p': Pawn}

        self.pgn = []

        # 50-move rule: after 50 half moves



    # TERMINAL METHODS

    def __str__(self):
        board_print = ''
        for i, row in enumerate(self.matrix):
            board_print += f'{8-i}   {" ".join(["-" if type(square)==int else square.char for square in row])}\n'
        board_print += '\n    A B C D E F G H'
        return board_print
    


    # MAIN METHODS
    
    def set_up_pieces(self):
        """Places piece objects on the board accorind to the FEN notation"""
        # Places piece objects on board
        for i in range(8):
            for j in range(8):
                if self.FEN[9*i+j] not in ["/", "-"]:
                    char = self.FEN[9*i+j]
                    # icon = self.fancyFEN[9*i+j]
                    Piece = self.piece_dict[char.lower()]
                    piece = Piece(i, j, char)
                    self.matrix[i, j] = piece


    def portable_game_notation(self, piece, target, inp):
        '''
        documents the moves as the game progresses, can be used later to compile a PGN 
        NOTE for game recording it is MUCH simpler to just record the cordinates pieces moved from and to and recreate from that
        '''
        char = piece.char.upper()
        move_notation = ''
        move_notation += char if char != 'P' else ''
        move_notation += 'x' if target else ''
        move_notation += inp[2:]

        self.pgn.append(move_notation)



# Program execution
chessgame = ChessGame()
chessgame.set_up_pieces()
print(chessgame)

while True:
    
    inp = input('from-to-coord: ')

    if len(inp) == 2:
        i, j = 8-int(inp[1]), ord(inp[0])-97
        piece = chessgame.matrix[i, j]
        if piece:
            print(f'piece info: {piece.char}, ({piece.i}, {piece.j})')
        else:
            print('empty square')
        continue

    if len(inp) == 4:
        i, j = 8-int(inp[1]), ord(inp[0])-97
        i2, j2 = 8-int(inp[3]), ord(inp[2])-97

        
        piece = chessgame.matrix[i, j]
        target = chessgame.matrix[i2, j2]

        try:
            piece.validator(i2, j2, chessgame.matrix)
            chessgame.portable_game_notation(piece, target, inp)


            # NOTE pawn just pushed must be excluded from list of pawns 

            # pieces = np.array(list(filter(lambda square: square != 0, chessgame.matrix.ravel())))
            # pawns = np.array(list(filter(lambda piece: piece.char.upper() == 'P', pieces)))
            # for pawn in pawns:
            #     pawn:Pawn
            #     pawn.last_move_double = False
            
        except AssertionError as err:
            traceback.print_exc()               # NOTE will also print AssertionError: custom message 
        
        print(chessgame.pgn)
        print(chessgame)        






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






# OLD


    # def update_legal_moves(self):
    #     """Updates legal moves for current pieces according to board state"""
    #     for piece in self.pieces_on_board:
    #         piece.assign_legal_moves(self.board)



    # def print_all_legal_moves(self):
    #     """Prints the legal moves of each piece"""
    #     for piece in self.pieces_on_board:
    #         print(piece.char, piece.legal_moves)   

#    def print_board(self):
#         """Prints a simple representation of the board in the terminal"""
#         for i in range(8):
#             print(8-i, end="    ")
#             for j in range(8):
#                 print(self.board[i, j], end=" ")
#             print()
#         print("\n     ", end="")
#         for i in range(8):
#             print(chr(i+65), end=" ")
#         print()
#         print(f"ctmm: {self.ctmm}")



#     def illustrate_move(self, from_square, to_square):
#         """Moves a piece to a square granted the move is legal"""
#         # Converts chess coordinate to matrix index
#         from_coord = f"{8-int(from_square[1])}{ord(from_square[0].upper())-65}"
#         to_coord = f"{8-int(to_square[1])}{ord(to_square[0].upper())-65}"
#         i1, j1 = int(from_coord[0]), int(from_coord[1])
#         i2, j2 = int(to_coord[0]), int(to_coord[1])
        
#         move = ChessRules(self, from_coord, to_coord)
#         if move.legality is True:
#             # Relocates and removes pieces, updates piece current position
#             if self.board[i2][j2] is not empty_square:
#                 target_piece = self.board[i2][j2]
#                 self.pieces_on_board.remove(target_piece)

#             self.board[i2][j2] = move.moving_piece
#             self.board[i1][j1] = empty_square

#             move.moving_piece.position = to_coord
#             self.update_legal_moves()

#             self.moves += 1
#             self.ctmm = ['w', 'b'][self.moves%2]
#             print(f"{from_coord} to {to_coord} was successful")
        
#         # Reprint board and pieces' moves
#         # self.print_all_legal_moves()
#         self.print_board()




    # def make_move(self, from_square: str, to_square: str) -> None:
    #     from_coord = f"{8-int(from_square[1])}{ord(from_square[0].upper())-65}"
    #     to_coord = f"{8-int(to_square[1])}{ord(to_square[0].upper())-65}"
    #     i, j = int(from_coord[0]), int(from_coord[1])
    #     i2, j2 = int(to_coord[0]), int(to_coord[1])

    #     piece = self.board[i, j]
    #     if piece.move_to(to_coord, self):
    #         piece.index = to_coord
    #         piece.i, piece.j = int(to_coord[0]), int(to_coord[1])

    #         self.board[i2, j2] = piece
    #         self.board[i, j] = empty_square
            
    #         self.moves += 1
    #         self.ctmm = ['w', 'b'][self.moves%2]
    #         print(f"{from_coord} to {to_coord} was successful")
    #     print(self)


    # def move_asker(self):
    #     while True:
    #         print(f'ctmm: {self.ctmm}')
    #         move = str(input("move piece [from-to] : ")).strip()
    #         from_square = move[:2]
    #         to_square = move[2:4]
    #         self.make_move(from_square, to_square)

