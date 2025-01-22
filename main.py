import piece
from board import Board
import display

# p1 = piece.L_piece(color="yellow", position=(0, 0))
# p2 = piece.I_piece(color="red", position=(1, 1))
# p3 = piece.L_piece(color="blue", position=(0, 0), angle=3)
# p4 = piece.L_piece(color="orange", position=(10, 8), angle=3)
p1 = piece.I_piece(color="yellow", position=(0, 3))
p2 = piece.I_piece(color="red", position=(0, 2))
p3 = piece.L_piece(color="blue", position=(0, 1), angle=3)
p4 = piece.L_piece(color="orange", position=(10, 8), angle=3)
p5 = piece.L_piece(color="green",position=(10,8),angle=1)
# p1.print_shape()

# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()


# p2.print_shape()

# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()

b = Board(width=10, height=20)

b.put_piece(p1)
b.put_piece(p2)
b.put_piece(p3,debug=True)
b.put_piece(p4)
b.put_piece(p5)
b.print_board()

if __name__ == "__main__":
    display.display(b)
