def read_input(filename):
    with open(filename) as file:
        grids = file.read().split("\n\n")

        locks = []
        keys = []

        for grid in grids:
            grid_split = grid.split("\n")
            
            if '.' not in grid_split[0]: # lock
                lock = []
                for i in range(len(grid_split[0])):
                    for j in range(len(grid_split)):
                        if grid_split[j][i] == ".":
                            break
                    lock.append(j-1)
                locks.append(lock)
            elif '.' not in grid_split[-1]: # key
                key = []
                for i in range(len(grid_split[0])):
                    for j in range(len(grid_split)):
                        if grid_split[len(grid_split)-j-1][i] == ".":
                            break
                    key.append(j-1)
                keys.append(key)
        return locks, keys

def check(lock, key):
    for i in range(5):
        height = 7
        if lock[i] + key[i] + 2 > height:
            return False
    return True

def check_pairs(locks, keys):
    total = 0
    for lock in locks:
        for key in keys:
            if check(lock, key):
                print(lock, key)
                total += 1
    return total

if __name__ == "__main__":
    locks, keys = read_input("input.txt")
    print(len(locks))
    print(len(keys))

    print(check_pairs(locks, keys))