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
            l = [h, v]
            shuffle(l)
            #s += l[0] + l[1] + "A"
            s = [k + h + v + "A" for k in s] + [k + v + h + "A" for k in s]
    return s

def dn(seq):
    s = ""
    for i in range(len(seq)):
        c1 = "A" if i == 0 else seq[i-1]
        c2 = seq[i]

        if c1 != c2:
            s += dmove(c1, c2)
        s += "A"
    return s

def dmove(c1, c2):
    mapping = {
        ("A", ">"): "v",
        ("A", "^"): "<",
        ("A", "v"): "<v",
        ("A", "<"): "v<<",
        ("^", ">"): ">v",
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
        ("v", "A"): ">^",
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

if __name__ == "__main__":
    codes = read_input("test.txt")
    #print(codes, [d1(code) for code in codes], [dn(d1(code)) for code in codes])
    total = 0
    for code in codes:
        d = d1(code)
        k = dapply(d, 2)
        lens = [len(s) for s in k]
        minlen = min(lens)
        print(code, lens, minlen)
        total += minlen * int(code.strip("A"))
    print(total)