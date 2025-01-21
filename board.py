from piece import Piece


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        #self.cell_size = cell_size
        self.board = [
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

    def print_board(self):
        b = self.board[::-1]
        for i in b:
            print("".join(["X" if j["fill"] else "." for j in i]))
