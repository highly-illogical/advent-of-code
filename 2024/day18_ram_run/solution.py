from collections import deque

class RAMRun:
    def __init__(self, filename, grid_size=7):
        self.grid_size = grid_size
        self.grid = [["." for j in range(grid_size)] for i in range(grid_size)]
        self._read_input(filename)

    def __repr__(self):
        return "\n".join(["".join([col for col in row]) for row in self.grid])

    def _read_input(self, filename):
        with open(filename) as file:
            bytes_list = [line.strip("\n").split(",") for line in file]
            self.bytes = [(int(x), int(y)) for x, y in bytes_list]

    def fallen_bytes(self, n):
        self.grid = [["." for j in range(self.grid_size)] for i in range(self.grid_size)]
        for i in range(n):
            x, y = self.bytes[i]
            self.grid[y][x] = "#"

    def bfs(self):
        start = (0, 0)
        goal = (self.grid_size-1, self.grid_size-1)
        horizon = deque()
        steps = [[None]*len(row) for row in self.grid]
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        horizon.append(start)
        steps[start[1]][start[0]] = 0 # x, y = j, i

        # Maintain horizon, list of visited squares
        while horizon:
            square = horizon.popleft()

            if square == goal:
                return steps[square[1]][square[0]]

            # Check neighbours
            for d in directions:
                p, q = square[0] + d[0], square[1] + d[1]

                if p in range(0, self.grid_size) and q in range(0, self.grid_size):
                    if self.grid[q][p] != "#" and steps[q][p] is None:
                        steps[q][p] = steps[square[1]][square[0]] + 1
                        horizon.append((p, q))

    def blocking_byte(self):
        for i in range(len(self.bytes)):
            self.fallen_bytes(i)
            steps = self.bfs()
            print(i, steps)
            if steps is None:
                return i, self.bytes[i-1]

if __name__ == "__main__":
    ram = RAMRun("input.txt", grid_size=71)
    #ram.fallen_bytes(1024)
    #print(ram)
    #print(ram.bfs())
    print(ram.blocking_byte())