import piece
from board import Board
import display

p1 = piece.L_piece(color="yellow", position=(0, 0))
p2 = piece.I_piece(color="red", position=(4, 4))
p3 = piece.L_piece(color="blue", position=(6, 6),angle=2)
# p1.print_shape()

# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()


# p2.print_shape()

# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()

b = Board(width=10,height= 20)
b.add_piece(p1)
b.add_piece(p2)
b.add_piece(p3)
b.print_board()

if __name__ == "__main__":
    display.display(b)
