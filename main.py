import piece
from board import Board
import display
from evaluation import Evaluation as ev
# import asyncio
import time


# p1 = piece.L_piece(color="yellow", position=(0, 0))
# p2 = piece.I_piece(color="red", position=(1, 1))
# p3 = piece.L_piece(color="blue", position=(0, 0), angle=3)
# p4 = piece.L_piece(color="orange", position=(10, 8), angle=3)
p1 = piece.I_piece(color="yellow", position=(19, 0), angle=0)
p2 = piece.I_piece(color="red", position=(19, 3), angle=0)
p3 = piece.I_piece(color="brown", position=(19, 6), angle=0)
p4 = piece.L_piece(color="blue", position=(17, 5), angle=3)
p5 = piece.L_piece(color="orange", position=(17, 8), angle=3)
p6 = piece.L_piece(color="green", position=(17, 8), angle=1)
p7 = piece.L_piece(color="purple", position=(17, 1), angle=3)
pt = piece.I_piece(color="yellow", position=(17, 9), angle=3)
# pt = piece.L_piece(color="yellow", position=(18, 1),angle=0)
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

# pieces = [pt ]#,p2,p3,p4]
# pieces = [p1 ,p2] #,p3,p4]
# pieces = [p1, p4,p2, p3,pt]  # ,p4]
pieces = [p1, p2, p3, pt, p4]  # , p5,p6,p7,pt]  # ,p4]
print(len(pieces))
# pieces = [p1, p2, p3 , p4,p5]
cleared_lines = 0
pieces_putted = 0
labels = {"score": 0, "lines": 0, "eval": 0}
e = ev()
if __name__ == "__main__":
    runnig = True
    while runnig:
        # rows_cleared = main_board.clear_rows()
        # if rows_cleared > 0:
        #     cleared_lines += 1
        #     print(f"Removed {rows_cleared} completed rows.")
        #     main_board.print_board()
        for p in pieces:
            # for p in piece.PieceGenerator(20):
            #    main_board.random_placement(p)
            first_time = True
            # print("-- next shape:")
            # p.print_shape()
            # print(p.get_position(),p.get_size())
            # print("---")
            actions = main_board.get_actions(p)
            for b in main_board.update_board_frames(p, actions):
                runnig = display.display(b,labels)
                time.sleep(0.18)
                if first_time:
                    time.sleep(0.6)
                    first_time = False
                b.print_board()
                print("---")
                if not runnig:
                    exit(0)
            main_board.put_piece(p)
            labels["score"] += 1
            labels["lines"] += main_board.clear_rows()
            labels["eval"] = e.evaluate(main_board)
            

        print("finished")
        print("Count of cleared lines ", labels['lines'])
        while runnig:
            runnig = display.display(main_board,labels)
