from collections import deque

class RaceCondition:
    def __init__(self, filename):
        self._read_input(filename)

        self.steps = [[None]*len(row) for row in self.track]
        self.steps[self.start[0]][self.start[1]] = 0
        self.found = []

    def __repr__(self):
        return "\n".join(["".join([s for s in row]) for row in self.track])

    def _read_input(self, filename):
        with open(filename) as file:
            self.track = [list(row.strip("\n")) for row in file]

            for i in range(len(self.track)):
                for j in range(len(self.track[i])):
                    if self.track[i][j] == 'S':
                        self.start = i, j
                    elif self.track[i][j] == 'E':
                        self.end = i, j

    def find_path(self):
        pos = self.start
        horizon = deque()
        horizon.append(pos)

        self.found = []

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while horizon:
            pos = horizon.popleft()
            self.found.append(pos)

            for d in directions:
                pos_new = pos[0] + d[0], pos[1] + d[1]

                if self.track[pos_new[0]][pos_new[1]] != "#":
                    if self.steps[pos_new[0]][pos_new[1]] is None:
                        self.steps[pos_new[0]][pos_new[1]] = self.steps[pos[0]][pos[1]] + 1
                        horizon.append(pos_new)

    def find_cheats(self):
        pos = self.start
        horizon = deque()
        horizon.append(pos)

        y = len(self.track)
        x = len(self.track[0])

        cheats = {}

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while horizon:
            pos = horizon.popleft()

            for d in directions:
                pos_new = pos[0] + d[0], pos[1] + d[1]

                if pos_new[0] in range(y) and pos_new[1] in range(x):
                    if self.track[pos_new[0]][pos_new[1]] == "#":
                        # check for cheats
                        for d in directions:
                            pos2 = pos_new[0] + d[0], pos_new[1] + d[1]

                            if pos2[0] in range(y) and pos2[1] in range(x):
                                if self.steps[pos2[0]][pos2[1]] is not None:
                                    diff = self.steps[pos2[0]][pos2[1]] - self.steps[pos[0]][pos[1]]
                                    if diff > 2:
                                        cheats[(pos, pos2)] = diff - 2

                    if self.track[pos_new[0]][pos_new[1]] != "#":
                        if self.steps[pos_new[0]][pos_new[1]] > self.steps[pos[0]][pos[1]]:
                            horizon.append(pos_new)
        return cheats

    def find_extended_cheats(self):
        pos = self.start
        horizon = deque()
        found = list()
        horizon.append(pos)

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        cheats = {}

        cheats_100 = 0

        while horizon:
            pos = horizon.popleft()

            for square in found:
                direct_diff = abs(pos[0] - square[0]) + abs(pos[1] - square[1])
                path_diff = self.steps[pos[0]][pos[1]] - self.steps[square[0]][square[1]]
                if direct_diff <= 20 and path_diff > direct_diff:
                    diff = path_diff - direct_diff
                    if diff >= 100:
                        cheats_100 += 1
                    '''if diff not in cheats:
                        cheats[diff] = [(square, pos)]
                    else:
                        if (square, pos) not in cheats[diff]:
                            cheats[diff].append((square, pos))'''
                    
            found.append(pos)

            for d in directions:
                pos_new = pos[0] + d[0], pos[1] + d[1]

                if self.steps[pos_new[0]][pos_new[1]] is not None:
                    if self.steps[pos_new[0]][pos_new[1]] > self.steps[pos[0]][pos[1]]:
                        horizon.append(pos_new)

        return cheats_100

    def find_cheats_by_path(self):
        def hadamard(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        cheats = {}

        for i in range(len(self.found)):
            for j in range(i+1, len(self.found)):
                prev = hadamard(self.found[i], self.found[j-1])
                current = hadamard(self.found[i], self.found[j])
                nxt = None

                if j + 1 < len(self.found):
                    nxt = hadamard(self.found[i], self.found[j+1])
                
                if prev > current and (current < nxt if nxt else True):
                    square = self.found[i]
                    pos = self.found[j]
                    direct_diff = current
                    path_diff = self.steps[pos[0]][pos[1]] - self.steps[square[0]][square[1]]
                    if direct_diff <= 20 and path_diff > direct_diff:
                        diff = path_diff - direct_diff
                        if diff not in cheats:
                            cheats[diff] = [(square, pos)]
                        else:
                            if (square, pos) not in cheats[diff]:
                                cheats[diff].append((square, pos))
        return cheats


if __name__ == "__main__":
    track = RaceCondition("input.txt")
    print(track)
    track.find_path()

    print(track.found)

    for row in track.steps:
        for col in row:
            print("  " if col is None else str(col) + " "*(col < 10), end="")
        print()

    #cheats = track.find_cheats()
    cheats_count = track.find_extended_cheats()
    #cheats_count = track.find_cheats_by_path()

    print(cheats_count)

    '''cheats_count = {}

    for val in set(cheats.values()):
        cheats_count[val] = []

    for key, val in cheats.items():
        cheats_count[val].append(key)

    for k in sorted(cheats_count.keys()):
        print(k, len(cheats_count[k]))'''

    '''total = 0
    for cheat, diff in cheats.items():
        if diff >= 100:
            total += 1
    print(total)'''