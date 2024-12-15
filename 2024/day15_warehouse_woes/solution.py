class WarehouseWoes:
    def __init__(self, filename):
        self.map = None
        self.expanded_map = None
        self.moves = None
        self.robot_pos = None
        self.robot_pos_expanded = None
        self.move_dict = {"^": (-1, 0), ">": (0, 1), "v": (1, 0), "<": (0, -1)}

        self.read_input(filename)
        self.create_expanded_map()

    def __repr__(self):
        s = ""
        for row in self.expanded_map:
            for col in row:
                s += col
            s += "\n"
        return s

    def read_input(self, filename):
        with open(filename) as file:
            map_string, move_string = file.read().split("\n\n")
            map_list = [list(s) for s in map_string.split("\n")]
            move_list = [m for m in move_string if m != "\n"]
            self.map = map_list
            self.moves = move_list
            self.robot_pos = self.get_robot_pos()

    def create_expanded_map(self):
        self.expanded_map = [[] for row in self.map]
        
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "O":
                    self.expanded_map[i].extend(["[", "]"])
                elif self.map[i][j] == "#":
                    self.expanded_map[i].extend(["#", "#"])
                elif self.map[i][j] == ".":
                    self.expanded_map[i].extend([".", "."])
                elif self.map[i][j] == "@":
                    self.expanded_map[i].extend(["@", "."])
                    self.robot_pos_expanded = i, 2*j
        return True

    def get_robot_pos(self):
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == '@':
                    return (i, j) # y, x
        return None

    def move(self, move_char):
        move = self.move_dict[move_char]
        i, j = self.robot_pos
        n = 0

        while self.map[i][j] in ['O', '@']:
            i, j = i + move[0], j + move[1]
            n += 1

        blocked = True if self.map[i][j] == "#" else False

        if not blocked:
            # print(n, (i, j))
            while (n > 0):
                self.map[i][j] = self.map[i - move[0]][j - move[1]]
                if self.map[i][j] == "@":
                    self.robot_pos = i, j
                i, j = i - move[0], j - move[1]
                n = n - 1
            self.map[i][j] = "."
            # print(self)
            return True

    def move_expanded(self, move_char):
        move = self.move_dict[move_char]
        return move
        
    def execute_moves(self):
        for m in self.moves:
            self.move(m)

    def sum_gps_coordinates(self):
        total = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "O":
                    total += i * 100 + j
        return total

if __name__ == "__main__":
    w = WarehouseWoes("test2.txt")
    print(w)
    #w.execute_moves()
    #print(w)
    #print(w.sum_gps_coordinates())