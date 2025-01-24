from piece import Piece
from copy import deepcopy , copy
import bfs
import random
import errno
from evaluation import Evaluation
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
        h , w = piece.get_size()
        try :
            for i in range(h):
                for j in range(w):
                    if shape[i][j] == "X":
                        self.board[i + x][j + y] = {
                            "color": piece.get_color(),
                            "fill": True,
                        }
        except IndexError:
            print("index error")
            print("x,y :", x, y, "h,w :", h, w,"i,j :", i, j)
            piece.print_shape()

    def clear_rows(self):
            new_board = []
            rows_removed = 0

            for row in self.board:
                if all(cell["fill"] for cell in row):  
                    rows_removed += 1
                else:
                    new_board.append(row)
            # Add empty rows to top 
            empty_row = [{"color": "white", "fill": False} for _ in range(self.width)]
            new_rows = [empty_row] * rows_removed

            self.board = new_board + new_rows
            return rows_removed

    def remove_piece(self, piece: Piece):
        shape = piece.get_shape()
        x, y = piece.get_position()
        h , w = piece.get_size()
        for i in range(h):
            for j in range(w):
                if shape[i][j] == "X":
                    self.board[i + x][j + y] = {"color": "white", "fill": False}

    def put_piece(self, piece: Piece, debug=False):
        def check_for_line(x1,x2):
            for i in range(x1,x2):
                if all(cell["fill"] for cell in self.board[i]):
                    return True
            return False
        for o in self.find_options(piece):
            pp_problem = PuttingPiece(piece=o, board=self)
            ans = bfs.BFS(problem=pp_problem)
            if not ans:
                continue
            else:
                path = bfs.trace_back(node=ans)
                self.add_piece(o)
                c = check_for_line(o.get_position()[0],o.get_position()[0]+o.get_size()[0])
                return path,c 

    # def put_piece(self, piece: Piece, debug=False):
    #     evaluator = Evaluation()
    #     best_score = float('-inf')
    #     best_path = None
    #     best_option = None

    #     for o in self.find_options(piece):
    #         # Solve the problem of placing the piece using BFS
    #         pp_problem = PuttingPiece(piece=o, board=self)
    #         ans = bfs.BFS(problem=pp_problem)

    #         # Trace back to get the path of the placement
    #         path = bfs.trace_back(node=ans)

    #         self.add_piece(o)
    #         score = evaluator.evaluate(self)  # Evaluate the board state
    #         self.remove_piece(o)  # Remove the piece after evaluation

    #         if debug:
    #             print(f"Option: {o}, Score: {score}")

    #         # Keep track of the best scoring option
    #         if score > best_score:
    #             best_score = score
    #             best_path = path
    #             best_option = o

    #     # If a best option is found, finalize the placement
    #     if best_option:
    #         self.add_piece(best_option)
    #         return best_path

    #     return None

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

    def has_space_to_rotate(self,x,y,h,w):
        try :
            for i in range(x, x + h):
                for j in range(y, y + w):
                    if self.board[i][j]["fill"]:
                        return False
        except IndexError:
            return False
        return True

    def can_rotate(self, piece: Piece,r):
        p = copy(piece)
        x, y = p.get_position()
        h, w = p.get_size()
        if h > w:
            if not self.has_space_to_rotate(x, y, h, w):
                return False
        r %=4
        if r==1:
            p.rotate(1)
            nx,ny =p.get_position()
            nh , nw = p.get_size()
            if (nx >= 0 and nx + nh < self.height) and (ny >= 0 and ny + nw < self.width):
                if not self.has_colision(p) :
                    if nh > nw:
                        if self.has_space_to_rotate(nx, ny, nh, nh):
                            return True
                        else :
                            return False
                    return True    
        elif r==3:
            p.rotate(3)
            nx,ny =p.get_position()
            nh , nw = p.get_size()
            if (nx >= 0 and nx + nh < self.height) and (ny >= 0 and ny + nw < self.width):
                if not self.has_colision(p) :
                    if nh > nw:
                        if self.has_space_to_rotate(nx, ny, nh, nh):
                            return True
                        else :
                            return False
                    return True      
        
        return False
    
    def has_colision(self, piece: Piece) -> bool:
        board = self.board
        shape = piece.get_shape()
        h, w = piece.get_size()
        x, y = piece.get_position()
        try:
            for i in range(0, h):
                for j in range(0, w):
                    if shape[i][j] == "X" and board[i + x][j + y]["fill"]:
                        return True
        except IndexError:
            print("index error")
            print("x,y :", x, y, "h,w :", h, w,"i,j :", i, j)
            piece.print_shape()
            self.print_board()
            exit(errno.EINVAL)
        return False

    def update_board_frames(self, piece: Piece, actions):
        board = self
        tmp_piece = piece
        for action in actions:
            x, y = tmp_piece.get_position()
            if action == "down":
                tmp_piece.set_position((x - 1, y))
            elif action == "left":
                tmp_piece.set_position((x, y - 1))
            elif action == "right":
                tmp_piece.set_position((x, y + 1))
            elif action == "rotate to right" :
                tmp_piece.rotate(1)
            elif action == "rotate to left":
                tmp_piece.rotate(3)
            board.add_piece(tmp_piece)
            yield board
            board.remove_piece(tmp_piece)

    def get_actions(self, piece: Piece):
        tmp_board = deepcopy(self)
        tmp_piece = deepcopy(piece)
        x , y = tmp_piece.get_position()
        path = tmp_board.put_piece(tmp_piece)[0]
        path = [p[1] for p in path ] # separating actions
        if not path:
            return False #can't put the new piece
        r_move = path.count("right")
        l_move = path.count("left")
        r_rotate = path.count("rotate to right")
        l_rotate = path.count("rotate to left")
        d = r_move - l_move
        if d < 0:
            d *= -1
            actions = d * ["left"]
        else:
            actions = d * ["right"]

        r = r_rotate - l_rotate
        if r < 0:
            r *= -1
            actions += r * ["rotate to left"]
        else:
            actions += r * ["rotate to right"]
        d_move = x - tmp_piece.get_position()[0] - path.count("down")
        actions += d_move * ["down"]
        for action in path[::-1]:
            if action == "down":
                actions += ["down"]
            elif action == "left":
                actions += ["right"]
            elif action == "right":
                actions += ["left"]
            elif action == "rotate to right":
                actions += ["rotate to left"]
            elif action == "rotate to left":
                actions += ["rotate to right"]
        actions = ["stay"] + actions
        return actions
    
    def random_placement(self,piece:Piece):
        x =  self.height - piece.get_size()[0]
        y = random.randint(0, self.width - piece.get_size()[1])
        piece.set_position((x, y))
        return piece
    
    def __eq__(self, other):
        return True if  self.board ==other.board and \
                        self.height == other.height and \
                        self.width ==other.width \
                        else False
    
    def __hash__(self):
        shape_t = tuple([tuple((cell["color"], cell["fill"]) for cell in row) for row in self.board])
        return hash(( shape_t, self.height,self.width))

    def clean(self):
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = {"color": "white", "fill": False}

class PuttingPiece:
    def __init__(self, piece: Piece, board: Board, enable=True):
        self.piece = piece
        self.board = board
        self.initial = (piece, board)
        self.enable = enable
        self.actions = ["down", "left", "right", "rotate to right", "rotate to left"]

    def is_goal(self, state: tuple[Piece, Board]):
        x, y = state[0].get_position()
        h, w = state[0].get_size()
        p = copy(state[0])
        #board = deepcopy(state[1])
        max_x = state[1].height
        #print("goal check: x,y,h,w", x, y, h, w)
        for i in range(x, max_x - h):  # could be better
            x = p.get_position()[0]
            p.set_position((x + 1, y))
            if state[1].has_colision(piece=p):
                return False
        else:
            return True

    def result(self, parent: bfs.Node, action):
        tmp_piece = copy(parent.state[0])
        
        x, y = tmp_piece.get_position()
        max_x, max_y = parent.state[1].height, parent.state[1].width
        if action == "down":
            tmp_piece.set_position((x + 1, y))
        elif action == "left":
            tmp_piece.set_position((x, y - 1))
        elif action == "right":
            tmp_piece.set_position((x, y + 1))
        elif action == "rotate to right":
            if parent.state[1].can_rotate(tmp_piece,1):
                tmp_piece.rotate(1)
            else:
                return None
        elif action == "rotate to left":
            if parent.state[1].can_rotate(tmp_piece,3):
                tmp_piece.rotate(3)
            else:
                return None

        h, w = tmp_piece.get_size()
        n_x, n_y = tmp_piece.get_position()
        if (n_x >= 0 and n_x + h < max_x) and (n_y >= 0 and n_y + w < max_y):
            if not parent.state[1].has_colision(tmp_piece):
                next_state = (tmp_piece, parent.state[1])
            else:
                return None
        else:
            return None

        node = bfs.Node(
            data=next_state, action=action, parent=parent, depth=parent.depth + 1
        )  # creating the node
        return node

