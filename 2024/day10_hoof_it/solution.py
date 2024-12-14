def read_input(filename):
    with open(filename) as file:
        trail_map = [list(line.strip('\n')) for line in file]
        trail_map = [[int(s) for s in row] for row in trail_map]
        return trail_map

def score(trail_map, distinct=False):
    score_map = []

    if not distinct:
        score_map = [[set([]) for col in row] for row in trail_map]
    else:
        score_map = [[0 for col in row] for row in trail_map]

    trailhead_score = 0

    for i in range(len(trail_map)):
        for j in range(len(trail_map[i])):
            if trail_map[i][j] == 9:
                if not distinct:
                    score_map[i][j] = score_map[i][j].union(set([(i, j)]))
                else:
                    score_map[i][j] = 1

    for i in range(9):
        num = 8 - i

        for i in range(len(trail_map)):
            for j in range(len(trail_map[i])):
                if trail_map[i][j] == num:

                    if 0 <= i + 1 < len(trail_map):
                        if trail_map[i + 1][j] == num + 1:
                            if distinct:
                                score_map[i][j] = score_map[i][j] + score_map[i + 1][j]
                            else:
                                score_map[i][j] = score_map[i][j].union(score_map[i + 1][j])

                    if 0 <= i - 1 < len(trail_map):
                        if trail_map[i - 1][j] == num + 1:
                            if distinct:
                                score_map[i][j] = score_map[i][j] + score_map[i - 1][j]
                            else:
                                score_map[i][j] = score_map[i][j].union(score_map[i - 1][j])

                    if 0 <= j + 1 < len(trail_map[i]):
                        if trail_map[i][j + 1] == num + 1:
                            if distinct:
                                score_map[i][j] = score_map[i][j] + score_map[i][j + 1]
                            else:
                                score_map[i][j] = score_map[i][j].union(score_map[i][j + 1])

                    if 0 <= j - 1 < len(trail_map):
                        if trail_map[i][j - 1] == num + 1:
                            if distinct:
                                score_map[i][j] = score_map[i][j] + score_map[i][j - 1]
                            else:
                                score_map[i][j] = score_map[i][j].union(score_map[i][j - 1])

                    if trail_map[i][j] == 0:
                        if distinct:
                            trailhead_score += score_map[i][j]
                        else:
                            trailhead_score += len(score_map[i][j])

    return score_map, trailhead_score


if __name__ == '__main__':
    trail_map = read_input("input.txt")
    print(score(trail_map, distinct=True))