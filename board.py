from piece import Piece
from copy import deepcopy


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # self.cell_size = cell_size
        self.board = [  # 2D array of cells. Each cell is a dictionary with color and fill properties
            [{"color": "white", "fill": False} for _ in range(width)]
            for _ in range(height)
        ]

    def add_piece(self, piece: Piece):
        shape = piece.get_shape()
        x, y = piece.get_position()
        for i in range(len(shape)):
            for j in range(len(shape)):
                if shape[i][j] == "X":
                    self.board[i + x][j + y] = {
                        "color": piece.get_color(),
                        "fill": True,
                    }

    def remove_piece(self, piece: Piece):
        shape = piece.get_shape()
        x, y = piece.get_position()
        for i in range(len(shape)):
            for j in range(len(shape)):
                if shape[i][j] == "X":
                    self.board[i + x][j + y] = {"color": "white", "fill": False}

    def put_piece(self, piece: Piece, debug=False):
        i = 0
        for o in self.find_options(piece):
            if i == 0:
                p = deepcopy(o)
            i += 1
            if debug:
                self.add_piece(o)
                self.print_board()
                self.remove_piece(o)
                print("-------")

        self.add_piece(p)

    def find_options(self, piece: Piece):
        h = self.height - piece.get_size()[0]
        p = piece
        y = p.position[1]
        for i in range(h):
            p.set_position((i, y))
            if not self.has_colision(p):
                yield p

    def print_board(self):
        b = self.board[::-1]
        for i in b:
            print("".join(["X" if j["fill"] else "." for j in i]))

    def has_colision(self, piece: Piece) -> bool:
        board = self.board
        shape = piece.get_shape()
        h, w = piece.get_size()
        x, y = piece.get_position()
        for i in range(0, h):
            for j in range(0, w):
                if shape[i][j] == "X" and board[i + x][j + y]["fill"]:
                    return True
        return False


class PuttingPiece:
    def __init__(self, piece: Piece, board: Board, enable=True):
        self.piece = piece
        self.board = board
        self.enable = enable
