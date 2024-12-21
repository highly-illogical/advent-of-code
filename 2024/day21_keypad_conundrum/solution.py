from random import shuffle

def read_input(filename):
    with open(filename) as file:
        return file.read().strip("\n").split("\n")

def numeric_position(s):
    mapping = {
        "7": (0, 0), "8": (1, 0), "9": (2, 0),
        "4": (0, 1), "5": (1, 1), "6": (2, 1),
        "1": (0, 2), "2": (1, 2), "3": (2, 2),
                     "0": (1, 3), "A": (2, 3)
    }
    return mapping[s]

def d1(code):
    s = [""]
    code = "A" + code

    for m, n in zip(code[:-1], code[1:]):
        mx, my = numeric_position(m)
        nx, ny = numeric_position(n)
        vertical = ny - my
        horizontal = nx - mx

        chh = ">" if horizontal > 0 else "<"
        chv = "v" if vertical > 0 else "^"

        v = chv*abs(vertical)
        h = chh*abs(horizontal)

        if mx == 0 and ny == 3:
            s = [k + h + v + "A" for k in s]
        elif my == 3 and nx == 0:
            s = [k + v + h + "A" for k in s]
        else:
            #l = [h, v]
            #shuffle(l)
            #s += l[0] + l[1] + "A"
            if horizontal < 0:
                s = [k + h + v + "A" for k in s]
            else:
                s = [k + v + h + "A" for k in s]
    return s

def dn(seq):
    seq = "A" + seq + "A"
    s = ""
    for i in range(1, len(seq)):
        c1 = seq[i-1]
        c2 = seq[i]

        if c1 != c2:
            s += dmove(c1, c2)
        s += "A"
    return s[:-1]

def dmove(c1, c2):
    mapping = {
        ("A", ">"): "v",
        ("A", "^"): "<",
        ("A", "v"): "<v",
        ("A", "<"): "v<<",
        ("^", ">"): "v>",
        ("^", "v"): "v",
        ("^", "<"): "v<",
        ("^", "A"): ">",
        (">", "^"): "<^",
        (">", "v"): "<",
        (">", "<"): "<<",
        (">", "A"): "^",
        ("v", ">"): ">",
        ("v", "^"): "^",
        ("v", "<"): "<",
        ("v", "A"): "^>",
        ("<", ">"): ">>",
        ("<", "^"): ">^",
        ("<", "v"): ">",
        ("<", "A"): ">>^"
    }

    return mapping[(c1, c2)]

def dapply(arr, n):
    arr_new = arr
    for i in range(n):
        arr_new = [dn(s) for s in arr_new]
    return arr_new

def split_groups(s):
    groups = []
    current = ""
    a_found = False
    a_count = 0
    for i in range(len(s)):
        if s[i] == "A":
            a_found = True
            a_count += 1
            continue
        if a_found and s[i] != "A":
            a_found = False
            groups.append(current)
            current = ""
        current = current + s[i]
    groups.append(current)
    return groups, a_count

def transform_group(g):
    i = 0
    while g[i] != "A":
        i = i + 1
    moves, activations = g[:i], g[i:]
    transformed_moves = dn(moves)
    groups = split_groups(transformed_moves)
    return transformed_moves, len(activations)

def extract_groups(tms):
    groups = []
    activations = []
    for tm in tms:
        groups.append(tm[0])
        activations.append(tm[1])
    return groups, activations

if __name__ == "__main__":
    codes = read_input("input.txt")

    #code = "029A"

    for code in codes:
        groups = d1(code)
        activations = 0

        for i in range(2):
            groups_new = []

            for group in groups:
                g, a = split_groups(dn(group))
                groups_new.extend(g)
                activations += a

            groups = groups_new

        print(groups, activations)
        print(sum(len(g) for g in groups) + activations)

        print(dn(dn(d1(code)[0])))

    