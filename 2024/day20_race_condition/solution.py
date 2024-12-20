from collections import deque

class RaceCondition:
    def __init__(self, filename):
        self._read_input(filename)

        self.steps = [[None]*len(row) for row in self.track]
        self.steps[self.start[0]][self.start[1]] = 0

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

        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

        while horizon:
            pos = horizon.popleft()

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

                                '''for d in directions:
                                    pos3 = pos2[0] + d[0], pos2[1] + d[1]

                                    if pos3[0] in range(y) and pos3[1] in range(x):
                                        if self.steps[pos3[0]][pos3[1]] is not None:

                                            if self.steps[pos2[0]][pos2[1]] is not None:
                                                if self.steps[pos3[0]][pos3[1]] < self.steps[pos2[0]][pos2[1]]:
                                                    continue

                                            diff = self.steps[pos3[0]][pos3[1]] - self.steps[pos[0]][pos[1]]
                                            if diff > 3:
                                                cheats[(pos, pos3)] = diff - 3'''

                    if self.track[pos_new[0]][pos_new[1]] != "#":
                        if self.steps[pos_new[0]][pos_new[1]] > self.steps[pos[0]][pos[1]]:
                            horizon.append(pos_new)
        return cheats

if __name__ == "__main__":
    track = RaceCondition("input.txt")
    print(track)
    track.find_path()

    for row in track.steps:
        for col in row:
            print("  " if col is None else str(col) + " "*(col < 10), end="")
        print()

    cheats = track.find_cheats()

    cheats_count = {}

    for val in set(cheats.values()):
        cheats_count[val] = []

    for key, val in cheats.items():
        cheats_count[val].append(key)

    for k in sorted(cheats_count.keys()):
        print(k, len(cheats_count[k]))

    total = 0
    for cheat, diff in cheats.items():
        if diff >= 100:
            total += 1
    print(total)