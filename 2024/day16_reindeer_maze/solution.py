class Node:
    def __init__(self, i, j, direction, blocked):
        self.i = i
        self.j = j
        self.direction = direction
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

        self.cost = [[None for col in row] for row in self.maze]
        self.cost[self.start[0]][self.start[1]] = 0

    def __repr__(self):
        return "\n".join(["".join(s) for s in self.maze])

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

    def clockwise(self, direction):
        return (direction + 1) % 4

    def counterclockwise(self, direction):
        return (direction - 1) % 4

    def find_paths(self):
        i, j = self.start
        forward = self.start_direction
        cw = (forward + 1) % 4
        ccw = (forward - 1) % 4

        horizon = [Node(*self.start, self.start_direction, False)]
        print(self.cost)

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
                        if self.cost[left_i][left_j] is None:
                            next_horizon.append(Node(node.i, node.j, ccw, False))
                    if self.maze[right_i][right_j] != "#":
                        if self.cost[right_i][right_j] is None:
                            next_horizon.append(Node(node.i, node.j, cw, False))

                    if self.maze[node.i + self.directions[direction][0]][node.j + self.directions[direction][1]] == '#':
                        node.blocked = True
                    else:
                        cost = self.cost[node.i][node.j]
                        node.i += self.directions[direction][0]
                        node.j += self.directions[direction][1]
                        if self.cost[node.i][node.j] is None:
                            self.cost[node.i][node.j] = cost + 1
                        else:
                            self.cost[node.i][node.j] = min(self.cost[node.i][node.j], cost + 1)

                        if self.maze[node.i][node.j] == "E":
                            return (self.cost[node.i][node.j] + 1000*n, direction)

                horizon = [node for node in horizon if not node.blocked]

            horizon = next_horizon
            n += 1
            print(horizon, n)
                
    '''def explore(self, i, j, direction):
        cost, forward = self.cost_dir[i][j]
        if cost is None:
            return
        clockwise = (forward + 1) % 4
        counterclockwise = (forward - 1) % 4

        p, q = i + self.directions[forward][0], j + self.directions[forward][1]
        to_explore = []
        while self.maze[p][q] != "#":
            for d in [self.directions[clockwise], self.directions[counterclockwise]]:
                if self.maze[p + d[0]][q + d[1]] != "#":
                    to_explore.append(((p, q), d))

            p, q = p + self.directions[forward][0], q + self.directions[forward][1]

    def get_neighbours(self, i, j, direction):
        dirs = [self.directions[direction], self.directions[(direction + 1) % len(self.directions)],
        self.directions[(direction - 1) % len(self.directions)]]

        neighbours = []
        for d in dirs:
            if self.maze[i + d[0]][j + d[1]] != "#":
                # self.maze[i + d[0]][j + d[1]] = "*"
                cost = self.cost[i][j]
                if d == self.directions[direction]:
                    cost += 1
                else:
                    cost += 1000
                neighbours.append(((i + d[0], j + d[1]), cost))

        return neighbours

    def find_paths(self):
        horizon = [(self.start, 0)]

        while len(horizon):
            # Get min cost node
            min_cost_node, min_cost = horizon[0]
            for node, node_cost in horizon:
                if node_cost < min_cost:
                    min_cost_node, min_cost = node, node_cost

            self.cost[min_cost_node[0]][min_cost_node[1]] = min_cost
            neighbours = self.get_neighbours(min_cost_node[0], min_cost_node[1], )

            for node in neighbours:
                pass'''


if __name__ == "__main__":
    maze = ReindeerMaze("input.txt")
    print(maze)
    print(maze.find_paths())

    '''for row in maze.cost:
        for col in row:
            print(col if col is not None else "-", end=" ")
        print()'''
