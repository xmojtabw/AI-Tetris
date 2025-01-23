import piece
from board import Board
import display
# import asyncio
import time


# p1 = piece.L_piece(color="yellow", position=(0, 0))
# p2 = piece.I_piece(color="red", position=(1, 1))
# p3 = piece.L_piece(color="blue", position=(0, 0), angle=3)
# p4 = piece.L_piece(color="orange", position=(10, 8), angle=3)
p1 = piece.I_piece(color="yellow", position=(17, 0),angle=1)
p2 = piece.I_piece(color="red", position=(19, 0))
p3 = piece.I_piece(color="brown", position=(19, 4))
p4 = piece.L_piece(color="blue", position=(17, 5), angle=3)
p5 = piece.L_piece(color="orange", position=(17, 8), angle=3)
p6 = piece.L_piece(color="green", position=(17, 8), angle=1)
p7 = piece.L_piece(color="purple", position=(17, 1),angle=3)
pt = piece.I_piece(color="yellow", position=(19, 1),angle=0)
#pt = piece.L_piece(color="yellow", position=(18, 1),angle=0)
# p1.print_shape()

# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()


# p2.print_shape()

# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()

main_board = Board(width=10, height=20)

# b.put_piece(p1)
# b.put_piece(p2)
# b.put_piece(p3,debug=True)
# b.put_piece(p4)
# b.put_piece(p5)

# b.add_piece(p1)

# b.print_board()

#pieces = [pt ]#,p2,p3,p4]
# pieces = [p1 ,p2] #,p3,p4]
pieces = [p1, p4,p2, p3,pt]  # ,p4]
# pieces = [p1, p2, p3 , p4,p5]
if __name__ == "__main__":
    runnig = True
    while runnig:
        #for p in pieces:
        for p in piece.PieceGenerator(20):
            main_board.random_placement(p)
            first_time = True
            # print("-- next shape:")
            # p.print_shape()
            # print(p.get_position(),p.get_size())
            # print("---")
            actions = main_board.get_actions(p)
            for b in main_board.update_board_frames(p, actions):
                runnig = display.display(b)
                time.sleep(0.18)
                if first_time:
                    time.sleep(0.6)
                    first_time=False
                b.print_board()
                print("---")
                if not runnig:
                    exit(0)
            main_board.put_piece(p)

        print("finished")
        while runnig:
            runnig = display.display(main_board)
