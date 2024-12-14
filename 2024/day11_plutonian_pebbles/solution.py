from tqdm import tqdm

def read_input(filename):
    with open(filename) as file:
        return [int(n) for n in file.read().strip("\n").split(" ")]

class Stones:
    def __init__(self, stones):
        self.stones = stones
        self.stones_dict = {}

        for stone in self.stones:
            self.stones_dict[stone] = self.stones.count(stone)

    def num_stones(self):
        return sum(self.stones_dict.values())

    def change_stone(self, i):
        s = str(self.stones[i])

        if self.stones[i] == 0:
            self.stones[i] = 1
            i += 1
        elif len(s) % 2 == 0:
            first, second = s[:len(s)//2], s[len(s)//2:]
            self.stones = self.stones[:i] + [int(first), int(second)] + self.stones[i+1:]
            i += 2
        else:
            self.stones[i] = self.stones[i] * 2024
            i += 1
        return i

    def blink(self):
        i = 0
        n = len(self.stones)
        while i < n:
            i = self.change_stone(i)
            n = len(self.stones)
        return i

    def blink_dict(self):
        new_dict = {}

        def add(k, v):
            if k not in new_dict:
                new_dict[k] = v
            else:
                new_dict[k] += v

        for key, value in self.stones_dict.items():
            if key == 0:
                add(1, value)
            elif len(str(key)) % 2 == 0:
                first, second = int(str(key)[:len(str(key))//2]), int(str(key)[len(str(key))//2:])
                add(first, value)
                add(second, value)
            else:
                add(key * 2024, value)

        self.stones_dict = new_dict

if __name__ == '__main__':
    stones = Stones(read_input("input.txt"))
    for i in range(75):
        stones.blink_dict()
    print(stones.num_stones())