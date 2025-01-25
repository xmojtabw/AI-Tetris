import multiprocessing.process
import piece
from board import Board
import display
from evaluation import Evaluation as ev
from agent import Agent
from sa_agent import SA_AGENT
import time
import multiprocessing
from copy import deepcopy, copy
import sys 

OPTIMIZE = True
alive = True


def SA_agent_task(queue, main_board: Board, display_ev, num_pieces=10):
    global alive
    while alive:
        pieces = [p for p in piece.PieceGenerator(num_pieces)]
        sa_agent = SA_AGENT(
            board_format=main_board,
            population_size=100,
            mutation_rate=0.01,
            answer_format=pieces,
            optimize=OPTIMIZE
        )
        ans = sa_agent.run(count=80)
        queue.put(ans)

        for p in ans:
            f, c = main_board.put_piece(copy(p), optimize=OPTIMIZE)
            if c:
                main_board.clear_rows()
            if not f:
                break
        main_board.print_board()
        display_ev.set()

        if f is None:
            print("Game Over")
            alive = False
            break



def agent_task(queue, main_board: Board, display_ev, num_pieces=10):
    global alive
    while alive:
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
            f, c = main_board.put_piece(copy(p), optimize=OPTIMIZE)
            if c:
                main_board.clear_rows()
            if not f:
                break
        main_board.print_board()
        display_ev.set()
        if f is None:
            print("Game Over")
            alive = False
            break


def display_task(queue,main_board:Board,display_ev ):
    labels = {"score": 0, "lines": 0, "eval": 0}
    runnig = True
    global alive
    e = ev()
    display.init_the_screen()
    while runnig:
        if queue.empty():
            if not alive:
                break
            display_ev.wait()
        ans = queue.get()
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
                time.sleep(0.3)
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




if __name__ == "__main__":
    try:
        option = sys.argv[1]
    except IndexError:
        print("'python main.py sa' for simulated annealing")
        print("'python main.py gen' for genetic algorithm")

    main_board = Board(width=10, height=20)
    queue = multiprocessing.Queue()
    display_ev = multiprocessing.Event()
    display_ev.clear()
    print(option)
    if option=="gen":
        computation_process = multiprocessing.Process(target=agent_task,args=(queue,deepcopy(main_board),display_ev,10))
    else:
        computation_process = multiprocessing.Process(
            target=SA_agent_task, args=(queue, deepcopy(main_board), display_ev, 10))

    display_process = multiprocessing.Process(
        target=display_task, args=(queue, deepcopy(main_board), display_ev))
    display_process.start()
    computation_process.start()

    computation_process.join()
    display_process.join()

