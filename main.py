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
GEN_POPULATION_SIZE = 250
GEN_MUTATION_RATE = 0.01
GEN_NUM_PIECES = 10
GEN_RUN_COUNT = 80

SA_POPULATION_SIZE = 150
SA_MUTATION_RATE = 0.01
SA_NUM_PIECES = 10
SA_RUN_COUNT = 80


def SA_agent_task(queue, main_board: Board, alive, num_pieces=10):
    while alive.value:
        pieces = [p for p in piece.PieceGenerator(num_pieces)]
        sa_agent = SA_AGENT(
            board_format=main_board,
            population_size=SA_POPULATION_SIZE,
            mutation_rate=SA_MUTATION_RATE,
            answer_format=pieces,
            optimize=OPTIMIZE
        )
        ans = sa_agent.run(count=SA_RUN_COUNT)
        queue.put(ans)

        for p in ans:
            f, c = main_board.put_piece(copy(p), optimize=OPTIMIZE)
            if c:
                main_board.clear_rows()
            if not f:
                break
        main_board.print_board()

        if f is None:
            print("Game Over")
            alive.value = False
            queue.put("finished")
            break



def agent_task(queue, main_board: Board, alive, num_pieces=10):
    while alive.value:
        pieces = [p for p in piece.PieceGenerator(num_pieces)]
        ag = Agent(
            board_format=main_board,
            population_size=GEN_POPULATION_SIZE,
            mutation_rate=GEN_MUTATION_RATE,
            answer_format=pieces,
            optimize=OPTIMIZE
        )
        ans = ag.run(count=GEN_RUN_COUNT)  
        queue.put(ans)
        for p in ans:
            f, c = main_board.put_piece(copy(p), optimize=OPTIMIZE)
            # main_board.print_board()
            # print("---")
            if c:
                main_board.clear_rows()
            if not f:
                break
        
        if f is None:
            print("Game Over")
            alive.value = False
            queue.put("finished")
            break


def display_task(queue,main_board:Board,alive ):
    def display_board(board,labels,count):
        for _ in range(count):
            runnig = display.display(board,labels)
            time.sleep(0.02)
            if not runnig:
                return False
        return True
        
    runnig = True
    labels = {"score": 0, "lines": 0, "eval": 0 , "wait":"Please wait ..."}
    e = ev() # evaluator
    display.init_the_screen()
    while runnig:
        while queue.empty():
            if alive.value:
                labels["wait"] = "Plese wait ..."
            else:
                labels["wait"] = "finished"
                runnig = False
                break
            runnig = display_board(main_board,labels,10)
            if not runnig:
                alive.value = False
                break
    
        ans = queue.get()
        if ans =="finished":
            break

        labels ["wait"] = False
        for p in ans:
            first_time = True
            # print("-- next shape:")
            # p.print_shape()
            # print(p.get_position(),p.get_size())
            # print("---")
            actions = main_board.get_actions(p,optimize=OPTIMIZE)
            if not actions or not runnig:
                break
            for b in main_board.update_board_frames(p, actions):
                runnig = display.display(b, labels)
                display_board(board=b,labels=labels,count=5)
                if first_time:
                    runnig = display_board(board=b,labels=labels,count=10)
                    first_time = False
                # b.print_board()
                # print("---")
                if not runnig:
                    alive.value = False
                    break
            main_board.put_piece(p,optimize=OPTIMIZE)
            labels["score"] += 1
            labels["lines"] += main_board.clear_rows()
            labels["eval"] = e.evaluate(main_board)
        
    alive.value = False
    runnig = True
    labels["wait"]= "finished"
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
        exit(1)

    main_board = Board(width=10, height=20)
    queue = multiprocessing.Queue()
    alive = multiprocessing.Value('b', True) 

    print(option)
    if option=="gen":
        computation_process = multiprocessing.Process(target=agent_task,args=(queue,deepcopy(main_board),alive,10))
    else:
        computation_process = multiprocessing.Process(
            target=SA_agent_task, args=(queue, deepcopy(main_board), alive, 10))

    display_process = multiprocessing.Process(
        target=display_task, args=(queue, deepcopy(main_board), alive))
    

    display_process.start()
    computation_process.start()

    computation_process.join()
    display_process.join()

