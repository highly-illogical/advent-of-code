def read_input(filename):
    with open(filename) as file:
        return [int(line.strip("\n")) for line in file]

def secret_number(start, n):
    while n > 0:
        start = ((start << 6) ^ start) % 16777216
        start = ((start >> 5) ^ start) % 16777216
        start = ((start << 11) ^ start) % 16777216
        n = n - 1
    return start

if __name__ == "__main__":
    start_nums = read_input("input.txt")
    
    print(sum(secret_number(num, 2000) for num in start_nums))