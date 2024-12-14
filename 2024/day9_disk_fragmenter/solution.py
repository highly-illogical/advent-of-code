def read_input(filename):
    with open(filename) as f:
        return [int(i) for i in f.read().strip('\n')]

def calculate_checksum(disk):
    num_files = sum(disk[::2])
    start = 0
    end = len(disk) - 1

    checksum = 0

    print(disk[::2])

    for file in range(num_files):
        free = start % 2 > 0

        if not free:
            checksum = checksum + (start // 2) * file
        else:
            checksum = checksum + (end // 2) * file
            disk[end] = disk[end] - 1

        disk[start] = disk[start] - 1

        while disk[start] == 0:
            start = start + 1
            free = not free

        while disk[end] == 0:
            end = end - 2

    print(sum(disk[::2]))

    return checksum

def calculate_checksum_file(file_id, length, start_index):
    return sum(file_id * k for k in range(start_index, start_index + length))

def calculate_checksum_whole(disk):
    files = disk[::2]
    moved = [None for file in files]
    free_space = disk[1::2]

    checksum = 0

    for i in range(len(files)):
        file_id = len(files) - i - 1
        length = files[-i-1]
        start_index = sum(disk[:file_id * 2])

        if sum(free_space) > 0:
            start = 0
            while start < len(files)-i-1:
                if free_space[start] < files[-i-1]:
                    start += 1
                else:
                    moved[-i-1] = start
                    start_index = sum(disk[:start * 2 + 1]) + (disk[start * 2 + 1] - free_space[start])
                    free_space[start] -= files[-i-1]
                    break

        checksum += calculate_checksum_file(file_id, length, start_index)

    return files, free_space, moved, checksum

if __name__ == '__main__':
    disk = read_input("input.txt")
    print(calculate_checksum_whole(disk))