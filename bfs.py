from queue import Queue , LifoQueue



class Node:
    def __init__(self, data, action=None, parent: "Node | None" = None, depth=0):
        self.state = data
        self.action = action
        self.parent = parent
        self.depth = depth


def expand(problem, node: Node):
    for action in problem.actions:
        child = problem.result(node, action)
        if child:  # if child is not none
            yield child


def BFS(problem):
    node = Node(data=problem.initial)
    if problem.is_goal(node.state):
        return node
    frontier = Queue()
    frontier.put(node)
    reached = {problem.initial}
    while not frontier.empty():
        node = frontier.get()
        for child in expand(problem, node):
            s = child.state
            if problem.is_goal(s):
                return child
            if s not in reached:
                reached.add(s)
                frontier.put(child)

    return None

def is_cycle(node: Node) -> bool:
    current = node #compare the node with all of it's parent
    while current.parent is not None:
        if current.parent.state == node.state:
            return True
        current = current.parent
    return False

def DLS(problem, limit=7):
    node = Node(problem.initial)
    frontier = LifoQueue()
    frontier.put(node)
    result = None
    while not frontier.empty():
        node = frontier.get()
        if problem.is_goal(node.state):
            return node
        if node.depth >= limit:
            result = "cut-off"

        elif not is_cycle(node):
            for child in expand(node=node, problem=problem):
                frontier.put(child)

    return result

def trace_back(node: Node) -> list:
    answers = []
    child = None
    while node:
        if child:
            answers.append([node.state, child.action])
        else:
            answers.append([node.state, "answer"])

        child = node
        node = node.parent
    return answers[::-1]
