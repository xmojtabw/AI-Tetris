from queue import Queue


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
