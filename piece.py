import random
import copy

class Piece:
    def __init__(
        self,
        shape: list,
        color="white",
        name="unknown piece",
        position=(0, 0),
        angle=0,
        h=0,
        w=0,
    ):
        self.name = name
        self.color = color
        self.shape = shape
        self.angle = angle  # each shape has 4 angles
        self.position = position  # position on the board
        self.h, self.w = h, w  # set the height and width for each piece
        self.shapes = [self.shape]
        s = self.shape
        for i in range(3):
            s = self._rotate(s)
            self.shapes.append(s)

        self.shapes = [self._stick_to_corner(i) for i in self.shapes]

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        result.position = self.position
        result.h = self.h
        result.w = self.w
        result.angle = self.angle
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            if k in ['position', 'h', 'w', 'angle']:
                setattr(result, k, copy.deepcopy(v, memo))
            else:
                setattr(result, k, v)
        return result
    def __str__(self):
        return f"{self.name} {self.color}"

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    def get_shape(self):  # get the current shape of the piece
        return self.shapes[self.angle]

    def set_color(self, color):
        self.color = color

    def set_name(self, name):
        self.name = name

    def set_position(self, position):
        self.position = position

    def get_position(self):
        return self.position

    def rotate(self, angle):
        self.angle += angle
        self.angle %= 4
        if self.angle % 2:
            self.position = (self.position[0] + self.h - self.w, self.position[1])
        else:
            self.position = (self.position[0] - self.h + self.w, self.position[1])
        return self

    def _rotate(self, shape: list) -> list:
        new_shape = [len(shape) * [0] for _ in range(len(shape[0]))]
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                new_shape[j][len(shape) - 1 - i] = shape[i][j]

        return new_shape

    def _stick_to_corner(self, shape: list) -> list:
        top_aligned_shape = [len(shape[0]) * ["."] for _ in range(len(shape))]

        # stick to buttom
        free_line_count = 0
        for i in range(len(shape)):
            if "X" not in shape[i]:
                free_line_count += 1
            else:
                break

        for i in range(len(shape) - free_line_count):
            top_aligned_shape[i] = shape[i + free_line_count]

        # stick to left
        aligned_shape = [len(shape[0]) * ["."] for _ in range(len(shape))]
        free_line_count = 0
        for i in range(len(top_aligned_shape[0])):
            if "X" not in [
                top_aligned_shape[j][i] for j in range(len(top_aligned_shape))
            ]:
                free_line_count += 1
            else:
                break

        for i in range(len(top_aligned_shape[0]) - free_line_count):
            for j in range(len(top_aligned_shape)):
                aligned_shape[j][i] = top_aligned_shape[j][i + free_line_count]

        return aligned_shape

    def print_shape(self):
        for i in self.shapes[self.angle]:
            print("".join(i))

    def set_angle(self, angle):
        self.angle = angle

    def get_size(self) -> tuple:  # get the height and and width of the current shape
        if self.angle % 2:
            return (self.w, self.h)
        else:
            return (self.h, self.w)

    def __eq__(self, other):
        return True if  self.position==other.position and \
                        self.shape == other.shape and \
                        self.angle==other.angle and \
                        self.color == other.color and \
                        self.h == other.h and self.w == other.w \
                        else False
    def __hash__(self):
        shape_t = tuple([tuple(_) for _  in self.get_shape()])
        return hash((self.position, shape_t, self.angle, self.color))

class L_piece(Piece):
    def __init__(self, color="white", position=(0, 0), angle=0, h=2, w=3):
        shape = [["X", "X", "X"], [".", ".", "X"], [".", ".", "."]]
        super().__init__(
            shape=shape,
            color=color,
            name="L piece",
            position=position,
            angle=angle,
            h=2,
            w=3,
        )


class I_piece(Piece):
    def __init__(self, color="white", position=(0, 0), angle=0):
        shape = [["X", "X", "X"], [".", ".", "."], [".", ".", "."]]
        super().__init__(
            shape=shape,
            color=color,
            name="I piece",
            position=position,
            angle=angle,
            h=1,
            w=3,
        )


def PieceGenerator(count):
    template_pieces = [I_piece, L_piece]
    colors = ["blue", "red", "green", "yellow", "purple", "orange", "pink", "brown"]
    for i in range(count):
        r = random.randint(0, len(template_pieces) - 1)
        color = random.randint(0, len(colors) - 1)
        angle = random.randint(0, 3)
        yield template_pieces[r](color=colors[color], angle=angle)
