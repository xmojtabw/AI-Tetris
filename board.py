from piece import Piece
from copy import deepcopy
import bfs

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
        for o in self.find_options(piece):
            pp_problem = PuttingPiece(piece=o,board=self)
            ans = bfs.BFS(problem=pp_problem)
            if not ans :
                continue
            else:
                if debug:
                    path = bfs.trace_back(node=ans)
                    i = 0
                    for w in path:
                        print(f"{i}: {w[1]}")
                        i += 1
                self.add_piece(o)
                break

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
        self.initial= (piece,board)
        self.enable = enable
        self.actions = ["down","left","right","rotate to right","rotate to left"]

    def is_goal(self,state:tuple[Piece,Board]):
        x , y = state[0].get_position()
        h , w = state[0].get_size()
        p = deepcopy(state[0])
        board = deepcopy(state[1])
        max_x = state[1].height
        for i in range(x,max_x-h): #could be better
            p.set_position((x+i,y))
            if board.has_colision(piece=p):
                return False
        else:
            return True
        
    def result(self, parent: bfs.Node, action):
        tmp_piece = deepcopy(parent.state[0])
        board = deepcopy(parent.state[1]) #change it later!
        x , y = tmp_piece.get_position()
        h , w = tmp_piece.get_size()
        max_x , max_y = board.height , board.width
        if action == "down":
            tmp_piece.set_position((x+1,y))
        if action == "left":
            tmp_piece.set_position((x,y+1))
        if action == "right":
            tmp_piece.set_position((x,y-1))
        if action == "rotate to right":
            tmp_piece.rotate(1)
        if action == "rotate to left":
            tmp_piece.rotate(3)
        
        n_x , n_y = tmp_piece.get_position()
        if (n_x >= 0 and n_x + h < max_x) and (n_y >= 0 and n_y + w < max_y ):
            if not board.has_colision(tmp_piece):
                next_state=(tmp_piece,board)
            else:
                return None
        else:
            return None
        
        node = bfs.Node(data=next_state, action=action,
                    parent=parent, depth=parent.depth + 1) #creating the node 
        return node


