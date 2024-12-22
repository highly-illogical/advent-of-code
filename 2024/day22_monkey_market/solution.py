def read_input(filename):
    with open(filename) as file:
        return [int(line.strip("\n")) for line in file]

def transform(start):
    start = ((start << 6) ^ start) % 16777216
    start = ((start >> 5) ^ start) % 16777216
    start = ((start << 11) ^ start) % 16777216
    return start

def prices(start):
    while True:
        yield start % 10
        start = transform(start)

def change_sequence(start):
    p = prices(start)
    previous = None
    current = next(p)

    while True:
        previous = current
        current = next(p)
        yield current - previous, current

def get_num_from_seq(sequence):
    return sum((sequence[-i-1]+9)*(19**i) for i in range(len(sequence)))

def get_seq_from_num(num):
    seq = []
    for i in range(4):
        seq.append((num % 19) - 9)
        num //= 19
    return seq[::-1]

def sell(start, sequence):
    seq = change_sequence(start)
    last4 = [None, None, None, None]
    i = 2000

    while i > 0:
        change, price = next(seq)
        last4 = last4[1:] + [change]

        if last4 == sequence:
            return price
        i = i - 1

def total_bananas(nums, sequence):
    total = 0
    for num in nums:
        price = sell(num, sequence)
        if price is not None:
            total += price
    return total

def calc_seq_prices(nums):
    seq_dict = {}

    for i in range(19**4):
        seq_dict[i] = [None]*len(nums)
    print("Memory allocated")

    for i in range(len(nums)):
        s = change_sequence(nums[i])
        last4 = 0
        for j in range(2000):
            change, price = next(s)
            last4 *= 19
            last4 += (change + 9)
            last4 %= 19**4

            if j >= 3:
                if seq_dict[last4][i] is None:
                    seq_dict[last4][i] = price

    max_seq = None
    max_bananas = 0
    for key, val in seq_dict.items():
        if sum(v for v in val if v is not None) > max_bananas:
            max_seq = key
            max_bananas = sum(v for v in val if v is not None)
    return get_seq_from_num(max_seq), max_bananas

def secret_number(start, n):
    while n > 0:
        start = transform(start)
        n = n - 1
    return start

if __name__ == "__main__":
    start_nums = read_input("input.txt")
    #print(len(start_nums))
    
    #print(sum(secret_number(num, 2000) for num in start_nums))
    print(calc_seq_prices(start_nums))
    #print(get_seq_from_num(19)) 
