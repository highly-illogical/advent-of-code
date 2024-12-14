from functools import lru_cache
from tqdm import tqdm

def read_input(filename):
    with open(filename) as file:
        machines = file.read().split("\n\n")
        machines = [machine.split("\n") for machine in machines]
        
        parsed_machines = []
        for machine in machines:
            parsed_machine = []
            for line in machine:
                coords = line.split(": ")[1].split(", ")
                coords = int(coords[0][2:]), int(coords[1][2:])
                parsed_machine.append(coords)
            parsed_machines.append(parsed_machine)
        return parsed_machines

@lru_cache
def cheapest_prize(a, b, prize):
    if prize[0] < 0 or prize[1] < 0:
        return None

    if prize[0] > (a[0] + b[0]) * 100:
        return None
    if prize[1] > (a[1] + b[1]) * 100:
        return None

    if prize == (0, 0):
        return 0

    push_a = cheapest_prize(a, b, (prize[0] - a[0], prize[1] - a[1]))
    push_b = cheapest_prize(a, b, (prize[0] - b[0], prize[1] - b[1]))
    
    if push_a is not None and push_b is not None:
        return min(3 + push_a, 1 + push_b)
    elif push_b is not None:
        return 1 + push_b
    elif push_a is not None:
        return 3 + push_a
    else:
        return None

def cheapest_prize_two(a, b, prize):
    '''
    94a + 22b = x
    34a + 67b = y
    94*(y - 67b) + 22*34b = 34*x
    94*y - 34*x = (94*67 - 22*34)b
    '''
    prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
    push_a = (prize[0]*b[1] - prize[1]*b[0]) // (a[0]*b[1] - a[1]*b[0])
    push_b = -(prize[0]*a[1] - prize[1]*a[0]) // (a[0]*b[1] - a[1]*b[0])

    if a[0] * push_a + b[0] * push_b == prize[0] and a[1] * push_a + b[1] * push_b == prize[1]:
        return 3 * push_a + push_b
    return None

if __name__ == "__main__":
    machines = read_input("input.txt")

    total = 0
    for machine in machines:
        cost = cheapest_prize_two(*machine)
        print(cost)
        if cost is not None:
            total += cost
    
    print("\n" + str(total))