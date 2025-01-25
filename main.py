import multiprocessing.process
import piece
from board import Board
import display
from evaluation import Evaluation as ev
from agent import Agent
import time
import multiprocessing
from copy import deepcopy, copy

OPTIMIZE = True
alive = True

def agent_task(queue,main_board:Board,display_ev,compute_ev=1, num_pieces=10):
    global alive
    while alive:
        # compute_ev.wait()
        pieces = [p for p in piece.PieceGenerator(num_pieces)]
        ag = Agent(
            board_format=main_board,
            population_size=250,
            mutation_rate=0.01,
            answer_format=pieces,
            optimize=OPTIMIZE
        )
        ans = ag.run(80)
        queue.put(ans)
        for p in ans:
            f,c = main_board.put_piece(copy(p),optimize=OPTIMIZE)
            if c:
                main_board.clear_rows()
            if not f: 
                break
        main_board.print_board()
        # compute_ev.clear()
        display_ev.set()
        if  f == None:
            print("Game Over")
            alive = False
            break


def display_task(queue,main_board:Board,display_ev ,compute_ev=1):
    labels = {"score": 0, "lines": 0, "eval": 0}
    runnig = True
    global alive
    e = ev()
    display.init_the_screen()
    while runnig:
        print("before wait")
        if queue.empty():
            if not alive:
                break
            display_ev.wait()
        print("after wait")
        ans = queue.get()
        # compute_ev.set()
        display_ev.clear()
        for p in ans:
            first_time = True
            # print("-- next shape:")
            # p.print_shape()
            # print(p.get_position(),p.get_size())
            # print("---")
            actions = main_board.get_actions(p,optimize=OPTIMIZE)
            if not actions:
                break
            for b in main_board.update_board_frames(p, actions):
                runnig = display.display(b, labels)
                time.sleep(0.1)
                if first_time:
                    time.sleep(0.7)
                    first_time = False
                # b.print_board()
                # print("---")
                if not runnig:
                    alive = False
                    break
            main_board.put_piece(p,optimize=OPTIMIZE)
            labels["score"] += 1
            labels["lines"] += main_board.clear_rows()
            labels["eval"] = e.evaluate(main_board)
        
    alive = False
    print("finished")
    print("Count of cleared lines ", labels["lines"])
    while runnig:
        runnig = display.display(main_board, labels)


# p1 = piece.L_piece(color="yellow", position=(0, 0))
# p2 = piece.I_piece(color="red", position=(1, 1))
# p3 = piece.L_piece(color="blue", position=(0, 0), angle=3)
# p4 = piece.L_piece(color="orange", position=(10, 8), angle=3)
p1 = piece.I_piece(color="yellow", position=(17, 0), angle=1)
p2 = piece.I_piece(color="red", position=(17, 6), angle=1)
p3 = piece.I_piece(color="brown", position=(19, 0), angle=0)
p4 = piece.L_piece(color="blue", position=(17, 1), angle=3)
p5 = piece.L_piece(color="orange", position=(17, 8), angle=3)
p6 = piece.L_piece(color="green", position=(17, 8), angle=1)
p7 = piece.L_piece(color="purple", position=(17, 1), angle=3)
pt = piece.I_piece(color="yellow", position=(19, 4), angle=0)
# pt = piece.L_piece(color="yellow", position=(18, 1),angle=0)
# p1.print_shape()

pa1 = piece.I_piece(color="yellow", position=(17, 6), angle=1)
pa2 = piece.I_piece(color="red", position=(19, 6), angle=0)
pa3 = piece.I_piece(color="brown", position=(19, 7), angle=0)

pb1 = piece.I_piece(color="yellow", position=(17, 3), angle=1)
pb2 = piece.I_piece(color="red", position=(19, 1), angle=0)
pb3 = piece.I_piece(color="brown", position=(19, 0), angle=0)

pc1 = piece.I_piece(color="yellow", position=(17, 3), angle=1)
pc2 = piece.I_piece(color="red", position=(19, 1), angle=0)
pc3 = piece.L_piece(color="brown", position=(18, 0), angle=0)

pa4 = piece.L_piece(color="blue", position=(17, 1), angle=3)
pa5 = piece.L_piece(color="orange", position=(17, 8), angle=3)
pa6 = piece.L_piece(color="green", position=(17, 8), angle=1)
pa7 = piece.L_piece(color="purple", position=(17, 1), angle=3)
pat = piece.I_piece(color="yellow", position=(19, 4), angle=0)
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()
# p1.rotate(1).print_shape()


# p2.print_shape()

# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()
# p2.rotate(1).print_shape()



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
#pieces = [p1, p2, p3,pt, p4]  # , p5,p6,p7,pt]  # ,p4]
#print(len(pieces))
#pieces = [p1, p2, p3 , p4,p5]
# pieces = [p for p in piece.PieceGenerator(10)]
#pieces = [pb1,pb2,pb3]
#pieces = [pa1,pa2,pa3]
#pieces = [pc1,pc2,pc3]

# cleared_lines = 0
# pieces_putted = 0


if __name__ == "__main__":
    main_board = Board(width=10, height=20)
    queue = multiprocessing.Queue()
    display_ev = multiprocessing.Event()
    display_ev.clear()
    computation_process = multiprocessing.Process(target=agent_task,args=(queue,deepcopy(main_board),display_ev,1,10))
    display_process = multiprocessing.Process(
        target=display_task, args=(queue, deepcopy(main_board), display_ev,1))
    display_process.start()
    computation_process.start()

    computation_process.join()
    display_process.join()

