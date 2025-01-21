from piece import *
from board import *
from display import *

p1 = L_piece(color="yellow", position=(0, 0))
p2 = I_piece(color="red", position=(4, 4))
# p1.print_shape()

# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()


# p2.print_shape()

# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()

b = Board(10, 10, 1)
b.add_piece(p1)
b.add_piece(p2)
b.print_board()

if __name__ == "__main__":
    display(b)
