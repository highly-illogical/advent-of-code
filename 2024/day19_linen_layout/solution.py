from functools import lru_cache

def read_input(filename):
    with open(filename) as file:
        towels, designs = file.read().split("\n\n")
        towels = towels.strip().split(", ")
        designs = designs.strip().split("\n")
        return towels, designs

if __name__ == "__main__":
    towels, designs = read_input("input.txt")
    print(towels, designs)

    @lru_cache
    def possible(design):
        i = 0

        if len(design) == 0:
            return True

        while i < len(design):
            if design[:i+1] in towels and possible(design[i+1:]):
                return True
            i += 1
        
        return False

    @lru_cache
    def ways(design):
        total = 0

        if len(design) == 0:
            return 1

        for i in range(len(design)):
            # if upto i as one towel in towels, add (ways to make rest of design) to total
            if design[:i+1] in towels:
                total += ways(design[i+1:])
        return total

    '''total = 0
    for design in designs:
        p = possible(design)
        if p:
            total += 1
        print(p)
    print(total)'''

    print(sum(ways(design) for design in designs))