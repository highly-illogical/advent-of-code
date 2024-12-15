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

    def is_blocked_expanded(self, move_char):
        move = self.move_dict[move_char]
        to_move = [(self.robot_pos_expanded[0], self.robot_pos_expanded[1])]

        while to_move:
            #print(to_move)
            for square in to_move:
                # Check if any squares are blocked directly by the next square
                i_new, j_new = square[0] + move[0], square[1] + move[1]
                if self.expanded_map[i_new][j_new] == "#":
                    return True
                    
            to_move_new = []
            for square in to_move:
                # Calculate next squares
                i_new, j_new = square[0] + move[0], square[1] + move[1]
                # print(square, i_new, j_new, self.expanded_map[i_new][j_new])
                if self.expanded_map[i_new][j_new] in ["[", "]"]:
                    to_move_new.append((i_new, j_new))
                if move_char in ["^", "v"]:
                    if self.expanded_map[i_new][j_new] == "[":
                        to_move_new.append((i_new, j_new + 1))
                    elif self.expanded_map[i_new][j_new] == "]":
                        to_move_new.append((i_new, j_new - 1))

            to_move = list(set(to_move_new))

        return False

    def copy_to_next(self, i, j, move):
        if self.map_expanded[i + move[0]][j + move[1]] != ".":
            self.copy_to_next(i + move[0], j + move[1], move)
        self.map_expanded[i + move[0]][j + move[1]] = self.map_expanded[i][j]
        self.map_expanded[i][j] = "."

    def move_expanded(self, move_char):
        move = self.move_dict[move_char]
        
        to_move_all = []

        if not self.is_blocked_expanded(move_char):
            to_move = [(self.robot_pos_expanded[0], self.robot_pos_expanded[1])]
            
            while to_move:
                to_move_all.append(to_move)
                        
                to_move_new = []
                for square in to_move:
                    # Calculate next squares
                    i_new, j_new = square[0] + move[0], square[1] + move[1]
                    if self.expanded_map[i_new][j_new] in ["[", "]"]:
                        to_move_new.append((i_new, j_new))
                    if move_char in ["^", "v"]:
                        if self.expanded_map[i_new][j_new] == "[":
                            to_move_new.append((i_new, j_new + 1))
                        elif self.expanded_map[i_new][j_new] == "]":
                            to_move_new.append((i_new, j_new - 1))

                to_move = list(set(to_move_new))
        else:
            #print("Blocked")
            return False
        
        for to_move in to_move_all[::-1]:
            for square in to_move:
                i, j = square
                i_next, j_next = i + move[0], j + move[1]
                self.expanded_map[i_next][j_next] = self.expanded_map[i][j]
                self.expanded_map[i][j] = "."
                if self.expanded_map[i_next][j_next] == "@":
                    self.robot_pos_expanded = i_next, j_next

    def execute_moves(self, expanded=True):
        for m in self.moves:
            if not expanded:
                self.move(m)
            else:
                self.move_expanded(m)

    def sum_gps_coordinates(self):
        total = 0
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] == "O":
                    total += i * 100 + j
        return total

    def sum_gps_coordinates_expanded(self):
        total = 0
        for i in range(len(self.expanded_map)):
            for j in range(len(self.expanded_map[i])):
                if self.expanded_map[i][j] == "[":
                    total += i * 100 + j
        return total

if __name__ == "__main__":
    w = WarehouseWoes("input.txt")
    print(w)
    w.execute_moves()
    print(w)
    print(w.sum_gps_coordinates_expanded())