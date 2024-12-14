def read_lists(filename: str) -> tuple[list[int], list[int]]:
    """Reads the two input lists from a file."""

    a = []
    b = []
    with open(filename) as file:
        for line in file:
            x, y = line.split("   ")
            a.append(int(x))
            b.append(int(y))
    return a, b

def distance_lists(a: list[int], b: list[int]) -> int:
    """Calculate the distance between the two lists."""

    if len(a) != len(b):
        raise ValueError("Lists must be the same length")
    a = sorted(a)
    b = sorted(b)
    return sum(abs(a[i] - b[i]) for i in range(len(a)))

def similarity_score(a: list[int], b: list[int]) -> int:
    """Calculate the similarity score between the two lists."""

    counts = {}
    score = 0

    for item in b:
        if item not in counts:
            counts[item] = 1
        else:
            counts[item] += 1

    for item in a:
        if item in counts:
            score += item * counts[item]
        
    return score

if __name__ == '__main__':
    a, b = read_lists("input.txt")
    print(similarity_score(a, b))