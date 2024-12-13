import re

def read_input(filename):
    with open(filename) as file:
        return file.read()

def find_uncorrupted(s, conditional=True):
    if conditional:
        pattern = r'do\(\)|don\'t\(\)|mul\([0-9]{1,3}\,[0-9]{1,3}\)'
    else:
        pattern = r'mul\([0-9]{1,3}\,[0-9]{1,3}\)'
    return re.findall(pattern, s)

def process_instructions(instructions):
    total = 0
    for mul in instructions:
        x, y = mul.lstrip("mul(").rstrip(")").split(",")
        total = total + int(x)*int(y)
    return total

def process_instructions_with_conditional(instructions):
    total = 0
    do = True
    for instruction in instructions:
        instruct_type, values = instruction.split("(")
        if instruct_type == "do":
            do = True
        elif instruct_type == "don't":
            do = False
        elif instruct_type == "mul":
            if do:
                x, y = values.rstrip(")").split(",")
                total += int(x) * int(y)
    return total

if __name__ == '__main__':
    s = read_input("input.txt")
    instructions = find_uncorrupted(s, conditional=False)
    print(process_instructions(instructions))