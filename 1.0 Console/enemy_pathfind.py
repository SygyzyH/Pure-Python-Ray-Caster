import random

game_map_test = [['#', '#', '#', '#', '#', '#', '#'],
                 ['#', '#', '#', '#', '#', '#', '#'],
                 ['#', '#', '#', '#', '#', '#', '#'],
                 ['.', '.', '.', 'e', '.', '.', '.'],
                 ['p', '.', '.', '.', '.', '.', '.'],
                 ['@', '.', '#', '.', '#', '.', '#'],
                 ['#', '.', '#', '.', '#', '.', '#']]
starting_position = [3, 3]


class Point:
    def __init__(self, x, y, connected, goal):
        self.x = x
        self.y = y
        self.connected = connected
        self.goal = goal
        self.hx = manhattan_dist(x, y, goal[0], goal[1])

    def get_as_list(self):
        return [self.x, self.y]

    def get_gx(self):
        if self.connected is None:
            return 0
        return self.connected.get_gx() + 1

    def get_fx(self):
        return self.get_gx() + self.hx

    def after_root(self):
        if self.connected.connected is None:
            return self
        else:
            return self.connected.after_root()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return str(self.x) + ", " + str(self.y) + " -> " + str(self.connected)


def pathfinder(game_map):
    global starting_position
    starting_position = [int(len(game_map)/2), int(len(game_map[0])/2)]
    return a_star(game_map, Point(starting_position[0], starting_position[1], None, find_player(game_map)), [], [])\
        .after_root().get_as_list()


def a_star(game_map: list, here: Point, opened: list, closed: list) -> Point:
    # if were in the correct place, we found it
    if game_map[here.y][here.x] == 'p':
        # solution found
        return here

    # update open list
    opened.extend(valid_moves(game_map, here, closed))

    # if there are no more options in open list
    if len(opened) == 0:
        # no solution found
        return random_valid(game_map)

    # sort by descending F(x)
    def fx_sort(e):
        return e.get_fx()
    opened.sort(key=fx_sort)
    decision = opened[0]

    # append decision to closed list
    closed.append(decision)

    # removed decision from opened list
    opened.remove(decision)

    # recurse
    return a_star(game_map, decision, opened, closed)


def valid_moves(game_map, here, closed):
    ans = []
    y = here.y
    x = here.x

    # take all moves that are in bounds and are not towards walls
    if 0 < y and game_map[y - 1][x] is not '#':
        ans.append(Point(x, y - 1, here, here.goal))
    if y < len(game_map[x]) - 1 and game_map[y + 1][x] is not '#':
        ans.append(Point(x, y + 1, here, here.goal))
    if 0 < x and game_map[y][x - 1] is not '#':
        ans.append(Point(x - 1, y, here, here.goal))
    if x < len(game_map) - 1 and game_map[y][x + 1] is not '#':
        ans.append(Point(x + 1, y, here, here.goal))

    # remove common values in closed
    ans = [i for i in ans if i not in closed]
    return ans


def random_valid(game_map):
    moves = valid_moves(game_map, Point(starting_position[0], starting_position[1], None, starting_position), [])
    return moves[random.randrange(len(moves))] if len(moves) != 0 else Point(starting_position[0], starting_position[1], None, starting_position)


def find_player(game_map):
    for line in game_map:
        if 'p' in line:
            return [line.index('p'), game_map.index(line)]
    return starting_position


def manhattan_dist(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)


def main():
    print(pathfinder(game_map_test))


if __name__ == "__main__":
    main()
