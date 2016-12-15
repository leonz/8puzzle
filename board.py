import random


GOAL = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, None]
]


class InvalidMoveException(Exception):
    pass


class Board:
    def __init__(self, tiles=None, times=10):
        if tiles is None:
            self.tiles = [row[:] for row in GOAL]
            self.scramble(times=times)
        else:
            self.tiles = [row[:] for row in tiles]

    def copy(self):
        return Board(tiles=[row[:] for row in self.tiles])

    def get_empty_coordinates(self):
        for x in range(len(self.tiles)):
            for y in range(len(self.tiles[x])):
                if self.tiles[x][y] is None:
                    return x, y

    def get_neighbor_coordinates(self, x, y):
        coordinates = []
        if x + 1 < len(self.tiles):
            coordinates.append((x + 1, y))
        if x > 0:
            coordinates.append((x - 1, y))
        if y + 1 < len(self.tiles[0]):
            coordinates.append((x, y + 1))
        if y > 0:
            coordinates.append((x, y - 1))
        return coordinates

    def scramble(self, times=5):
        for i in range(times):
            self.move_random()

    def move_random(self):
        x, y = self.get_empty_coordinates()
        neighbors = self.get_neighbor_coordinates(x, y)
        x_dest, y_dest = random.choice(neighbors)
        self.tiles[x][y] = self.tiles[x_dest][y_dest]
        self.tiles[x_dest][y_dest] = None

    def move_up(self):
        x, y = self.get_empty_coordinates()
        neighbors = self.get_neighbor_coordinates(x, y)
        if (x - 1, y) in neighbors:
            self.tiles[x][y] = self.tiles[x-1][y]
            self.tiles[x-1][y] = None
        else:
            raise InvalidMoveException()

    def move_down(self):
        x, y = self.get_empty_coordinates()
        neighbors = self.get_neighbor_coordinates(x, y)
        if (x + 1, y) in neighbors:
            self.tiles[x][y] = self.tiles[x+1][y]
            self.tiles[x+1][y] = None
        else:
            raise InvalidMoveException()

    def move_left(self):
        x, y = self.get_empty_coordinates()
        neighbors = self.get_neighbor_coordinates(x, y)
        if (x, y - 1) in neighbors:
            self.tiles[x][y] = self.tiles[x][y-1]
            self.tiles[x][y - 1] = None
        else:
            raise InvalidMoveException()

    def move_right(self):
        x, y = self.get_empty_coordinates()
        neighbors = self.get_neighbor_coordinates(x, y)
        if (x, y + 1) in neighbors:
            self.tiles[x][y] = self.tiles[x][y+1]
            self.tiles[x][y + 1] = None
        else:
            raise InvalidMoveException()

    def solved(self):
        return self.tiles == GOAL

    def show(self):
        for row in self.tiles:
            print(', '.join((str(x) for x in row)))

    def hamming(self):
        """ Returns count of out-of-place tiles. """
        wrong_count = 0
        expected = 1
        for row in self.tiles:
            for tile in row:
                if expected == 9:
                    return wrong_count
                if not tile == expected:
                    wrong_count += 1
                expected += 1

    def manhattan(self):
        """ Returns the total distance of out-of-place tiles to their
        correct locations via Manhattan distance. """
        distance = 0
        goal_coordinates = {}
        current_coordinates = {}
        for x in range(len(GOAL)):
            for y in range(len(GOAL[0])):
                goal_coordinates[GOAL[x][y]] = (x, y)
                current_coordinates[self.tiles[x][y]] = (x, y)

        for i in range(1, 9):
            current_x, current_y = current_coordinates[i]
            goal_x, goal_y = goal_coordinates[i]
            distance_x = current_x - goal_x
            distance_y = current_y - goal_y
            distance += abs(distance_x) + abs(distance_y)

        return distance


if __name__ == '__main__':
    board = Board()
    board.show()
    print('Starting game.')
    num_moves = 0
    while not board.solved():
        try:
            move = input('Enter a move: ')
            if move == 'u':
                board.move_up()
            elif move == 'd':
                board.move_down()
            elif move == 'r':
                board.move_right()
            elif move == 'l':
                board.move_left()
            elif move in ('x', 'q'):
                break
            else:
                print('Invalid command.')
            num_moves += 1
            board.show()
        except:
            print('Invalid move.')

    print('Finished in %s moves.' % num_moves)
