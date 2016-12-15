import random
from collections import namedtuple
from board import InvalidMoveException

State = namedtuple('State', ['board', 'moves', 'previous'])


class PriorityQueue():
    def __init__(self):
        self.queue = []

    def put(self, priority, item):
        self.queue.append((priority, item))

    def get(self):
        self.queue.sort(key=lambda x: x[0])
        return self.queue.pop(0)


class AI:
    def __init__(self, board):
        self.board = board
        self.moves = 0

    def make_move(self):
        raise NotImplemented()


class AStarAI(AI):
    def __init__(self, board):
        super(AStarAI, self).__init__(board)

    def make_move(self):
        self.pqueue = PriorityQueue()
        self.pqueue.put(0, State(self.board.copy(), [], None))

        while not self.board.solved():
            _, state = self.pqueue.get()
            self.board = state.board
            if self.board.solved():
                if len(state.moves) == 0:
                    return 'r'  # doesn't matter
                return state.moves[0]

            new_boards = []

            try:
                board = state.board.copy()
                board.move_up()
                new_boards.append((board, "u"))
            except InvalidMoveException:
                pass
            try:
                board = state.board.copy()
                board.move_down()
                new_boards.append((board, "d"))
            except InvalidMoveException:
                pass
            try:
                board = state.board.copy()
                board.move_right()
                new_boards.append((board, "r"))
            except InvalidMoveException:
                pass
            try:
                board = state.board.copy()
                board.move_left()
                new_boards.append((board, "l"))
            except InvalidMoveException:
                pass

            for board, move in new_boards:
                new_moves = list(state.moves)
                new_moves.append(move)
                self.pqueue.put(
                    len(state.moves) + board.manhattan(),
                    State(board, new_moves, state.board)
                )


class HammingAI(AStarAI):
    def __init__(self):
        super(HammingAI, self).__init__()

    def priority(self, board):
        return board.hamming()


class ManhattanAI(AStarAI):
    def __init__(self):
        super(ManhattanAI, self).__init__()

    def priority(self, board):
        return board.manhattan()


class GreedyAI(AI):
    def __init__(self, board):
        super(AI, self).__init__()
        self.board = board

    def make_move(self):
        heuristic = self.board.manhattan()
        move = None

        try:
            board = self.board.copy()
            board.move_up()
            if board.manhattan() < heuristic:
                heuristic = board.manhattan()
                move = 'u'
        except InvalidMoveException:
            pass
        try:
            board = self.board.copy()
            board.move_down()
            if board.manhattan() < heuristic:
                heuristic = board.manhattan()
                move = 'd'
        except InvalidMoveException:
            pass
        try:
            board = self.board.copy()
            board.move_right()
            if board.manhattan() < heuristic:
                heuristic = board.manhattan()
                move = 'r'
        except InvalidMoveException:
            pass
        try:
            board = self.board.copy()
            board.move_left()
            if board.manhattan() < heuristic:
                heuristic = board.manhattan()
                move = 'l'
        except InvalidMoveException:
            pass

        if move is None:
            move = random.choice(('u', 'd', 'l', 'r'))

        return move


class RandomAI(AI):
    def __init__(self):
        super(RandomAI, self).__init__()

    def make_move(self):
        return random.choice(('u', 'd', 'l', 'r'))

#
#if __name__ == '__main__':
#    from board import Board
#    times = 20
#    board2 = Board(times=times)
#    print("Board shuffled %i times" % times)
#    bot = AStarAI(board2)
#    moves = 0
#    while not bot.board.solved():
#        moves = bot.make_move()
#        print("----- move %i" % moves)
#        bot.board.show()
#        sleep(1)
#    print("Solved in %i moves using A* search." % moves)
