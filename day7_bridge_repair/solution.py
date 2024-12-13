from tqdm import tqdm

def read_input(filename):
    input_list = []
    with open(filename) as file:
        for line in file:
            result, operands = line.strip("\n").split(": ")
            operands = operands.split(" ")
            result = int(result)
            operands = tuple(map(lambda x: int(x), operands))
            input_list.append((result, operands))
    return input_list

def can_produce_value(value, operands):
    if len(operands) == 1:
        return operands[0] == value

    if len(operands) > 1:
        if value % operands[-1] == 0:
            return can_produce_value(value // operands[-1], operands[:-1]) or can_produce_value(value - operands[-1], operands[:-1])
        else:
            return can_produce_value(value - operands[-1], operands[:-1])

def can_produce_value_left(value, operands):
    if len(operands) == 1:
        return operands[0] == value

    if len(operands) > 1:
        return can_produce_value_left(value, (operands[0] + operands[1], *operands[2:])) or can_produce_value_left(value, (operands[0] * operands[1], *operands[2:])) or can_produce_value_left(value, (int(str(operands[0]) + str(operands[1])), *operands[2:]))

def total_calibration_result(inputs):
    return sum(item[0] for item in tqdm(inputs) if can_produce_value_left(*item))

if __name__ == '__main__':
    inputs = read_input("input.txt")
    print(total_calibration_result(inputs))