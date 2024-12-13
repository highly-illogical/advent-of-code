import tqdm

class GuardGallivant:
    def __init__(self, filename):
        self.filename = filename
        self.map = self._read_input(filename)
        self.start_position = None
        self.start_direction = None
        self.position = None
        self.direction = None
        self.positions_visited = 0

        self.obstacle_loops = [[None for col in row] for row in self.map]

        self._init_guard_position()

    def __repr__(self):
        return "\n".join(["".join(r) for r in self.map]) + f"\nThe guard is at {self.position} facing {self.direction}."

    def _read_input(self, filename):
        with open(filename) as file:
            return [list(line.strip("\n")) for line in file.readlines()]

    def _init_guard_position(self):
        directions = {"^": "up", "<": "left", ">": "right", "v": "down"}
        self.map_directions = [[{"up": False, "left": False, "right": False, "down": False} for col in row] for row in self.map]
        
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in directions:
                    self.position = i, j
                    self.direction = directions[self.map[i][j]]
                    self.start_position = i, j
                    self.start_direction = self.map[i][j]
                    self._add_map_direction()
                    self.positions_visited = 1
                    return self.position, self.direction

    def _mark_position(self, mark):
        self.map[self.position[0]][self.position[1]] = mark
        return self.position

    def _add_map_direction(self):
        # print(self.position, self.direction, self.map_directions[self.position[0]][self.position[1]][self.direction])
        if self.map_directions[self.position[0]][self.position[1]][self.direction]:
            return "loop"
        self.map_directions[self.position[0]][self.position[1]][self.direction] = True
        return self.direction

    def move(self):
        move_dict = {"up": (-1, 0), "left": (0, -1), "right": (0, 1), "down": (1, 0)}
        mark_dict = {"up": "|", "left": "-", "right": "-", "down": "|"}

        while True:
            # print(self.position, self.direction)
            new_position = (self.position[0] + move_dict[self.direction][0], self.position[1] + move_dict[self.direction][1])
            
            if new_position[0] < 0 or new_position[0] >= len(self.map) or new_position[1] < 0 or new_position[1] >= len(self.map[0]):
                return self.position

            if self.map[new_position[0]][new_position[1]] in ["#", "O"]:
                self.turn_right()
                self._mark_position("+")
                if self._add_map_direction() == "loop":
                    #print("The guard is in a loop.")
                    return -1
            else:
                self.position = new_position
                if self._add_map_direction() == "loop":
                    #print("The guard is in a loop.")
                    return -1
                if self.map[self.position[0]][self.position[1]] == ".":
                    self.positions_visited += 1
                    self._mark_position(mark_dict[self.direction])

        return self.position

    def check_loop(self):
        return self.move() == -1

    def reset(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] != "#":
                    self.map[i][j] = '.'

        self.map[self.start_position[0]][self.start_position[1]] = self.start_direction
        self.position = None
        self.direction = None
        self.positions_visited = 0

        self._init_guard_position()

    def check_loops_with_obstacles(self):
        for i in tqdm.tqdm(range(len(self.obstacle_loops))):
            for j in range(len(self.obstacle_loops[i])):
                # print(i, j)
                self.reset()

                if self.map[i][j] not in ["#", "^", ">", "v", "<"]:
                    self.map[i][j] = "O"
                    self.obstacle_loops[i][j] = self.check_loop()
        
        return sum(sum(1 for loop in self.obstacle_loops[i] if loop) for i in range(len(self.obstacle_loops)))
            
    def turn_right(self):
        right_turn_dict = {"up": "right", "right": "down", "down": "left", "left": "up"}
        self.direction = right_turn_dict[self.direction]
        return self.direction


if __name__ == '__main__':
    guard = GuardGallivant("input.txt")
    print(guard.check_loops_with_obstacles())
    # print(guard.obstacle_loops)
    # print(guard)