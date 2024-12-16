# Have to keep track of n (number of turns) to get to the same position *and* facing the same direction
# This code counts extra paths that require more turns to get to the same position facing the same direction

class Node:
    def __init__(self, i, j, direction, add_turn_cost, blocked):
        self.i = i
        self.j = j
        self.direction = direction
        self.add_turn_cost = False
        self.blocked = blocked

    def __repr__(self):
        return f"({self.i}, {self.j}, {self.direction}, {self.blocked})"

class ReindeerMaze:
    def __init__(self, filename):
        self.maze = None
        self.start = None
        self.end = None
        self.start_direction = 0
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        self._read_input(filename)

        self.cost = [[[None]*4 for col in row] for row in self.maze]
        self.cost[self.start[0]][self.start[1]][self.start_direction] = 0

        self.previous_tiles = [[list() for col in row] for row in self.maze]

    def __repr__(self):
        return "\n".join([" ".join((str(i) for i in s)) for s in self.maze])

    def _read_input(self, filename):
        with open(filename) as file:
            self.maze = [list(s.strip("\n")) for s in file.readlines()]
            for i in range(len(self.maze)):
                for j in range(len(self.maze[i])):
                    if self.maze[i][j] == "S":
                        self.start = i, j
                    if self.maze[i][j] == "E":
                        self.end = i, j
            return True

    def get_cost(self, cost, n):
        return cost + n*1000

    def clockwise(self, direction):
        return (direction + 1) % 4

    def counterclockwise(self, direction):
        return (direction - 1) % 4

    def find_paths(self):
        i, j = self.start
        forward = self.start_direction
        cw = (forward + 1) % 4
        ccw = (forward - 1) % 4

        horizon = [Node(*self.start, self.start_direction, False, False)]

        # for each element on horizon
        # check to both sides -> if free, append to next horizon list
        # if no wall ahead, move forward, update new square cost

        n = 0 # number of turns
        while True:
            next_horizon = []

            while len(horizon):
                for node in horizon:
                    direction = node.direction
                    cw, ccw = self.clockwise(direction), self.counterclockwise(direction)

                    left_i, left_j = node.i + self.directions[ccw][0], node.j + self.directions[ccw][1]
                    right_i, right_j = node.i + self.directions[cw][0], node.j + self.directions[cw][1]

                    if self.maze[left_i][left_j] != "#":
                        if self.cost[left_i][left_j][ccw] is None:
                            self.cost[node.i][node.j][ccw] = self.cost[node.i][node.j][direction] + 1000 # turn
                            next_horizon.append(Node(node.i, node.j, ccw, True, False))
                    if self.maze[right_i][right_j] != "#":
                        if self.cost[right_i][right_j][cw] is None:
                            self.cost[node.i][node.j][cw] = self.cost[node.i][node.j][direction] + 1000 # turn
                            next_horizon.append(Node(node.i, node.j, cw, True, False))

                    if self.maze[node.i + self.directions[direction][0]][node.j + self.directions[direction][1]] == '#':
                        node.blocked = True
                    else:
                        cost = self.cost[node.i][node.j][direction]
                        i, j = node.i, node.j
                        node.i += self.directions[direction][0]
                        node.j += self.directions[direction][1]

                        if self.cost[node.i][node.j][direction] is None:
                            self.cost[node.i][node.j][direction] = cost + 1
                            #self.previous_tiles[node.i][node.j].append(((i, j, direction), cost))
                        else:
                            # print(node.i, node.j, self.cost[node.i][node.j], cost + 1)
                            if self.cost[node.i][node.j][direction] >= cost + 1:
                                self.cost[node.i][node.j][direction] = cost + 1
                                #self.previous_tiles[node.i][node.j][(direction + 2) % 4] = cost

                        if self.maze[node.i][node.j] == "E":
                            return (min(c for c in self.cost[node.i][node.j] if c is not None), direction)

                horizon = [node for node in horizon if not node.blocked]

            horizon = list(set(next_horizon))
            n += 1
            # print(horizon, n)
                
    def tiles_on_best_path(self):
        horizon = [(self.end[0], self.end[1], 3)]
        tiles = 1

        while horizon:
            next_horizon = []
            for i, j, direction in horizon:
                    if self.cost[i][j][(direction + 1) % 4] == self.cost[i][j][direction] - 1000:
                        next_horizon.append((i, j, (direction+1) % 4))
                    if self.cost[i][j][(direction - 1) % 4] == self.cost[i][j][direction] - 1000:
                        next_horizon.append((i, j, (direction-1) % 4))
                    if self.cost[i - self.directions[direction][0]][j - self.directions[direction][1]][direction] == self.cost[i][j][direction] - 1:
                        next_horizon.append((i - self.directions[direction][0], j - self.directions[direction][1], direction))
                        self.maze[i - self.directions[direction][0]][j - self.directions[direction][1]] = "O"
            horizon = list(set(next_horizon))
            #print(n, tiles, horizon)

        return True

if __name__ == "__main__":
    maze = ReindeerMaze("input.txt")
    print(maze.find_paths())
    maze.tiles_on_best_path()
    #print(maze)

    tiles = 0
    for row in maze.maze:
        for col in row:
            if col not in ['#', "."]:
                tiles += 1
    print(tiles)

    '''for row in maze.cost:
        for col in row:
            print(((" "*(col // 100 == 0)) + (" "*(col // 10 == 0)) + str(col)) if col is not None else " -1", end=" ")
        print()'''
