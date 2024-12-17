import math

class ThreeBitNumber:
    def __init__(self, num):
        self.num = num
        self.next = None

class ChronospatialComputer:
    def __init__(self, filename):
        self.registers = {}
        self.program = ""
        self.instruction_pointer = None
        self.output = []

        #self.match_pointer = 0

        self._read_input(filename)

    def __repr__(self):
        return (f'A: {self.registers["A"]}, B: {self.registers["B"]}, C: {self.registers["C"]}\n{", ".join([str(s) for s in self.program])}')

    def _read_input(self, filename):
        with open(filename) as file:
            registers, program = file.read().split("\n\n")
            registers = registers.strip("\n").split("\n")

            for register in registers:
                name, value = register.split(": ")
                if name == "Register A":
                    self.registers["A"] = int(value)
                if name == "Register B":
                    self.registers["B"] = int(value)
                if name == "Register C":
                    self.registers["C"] = int(value)

            _, instructions = program.split(": ")
            self.program = [int(inst) for inst in instructions.split(",")]

            self.instruction_pointer = 0

    def combo(self, operand):
        if operand in range(4):
            return operand
        if operand == 4:
            return self.registers["A"]
        if operand == 5:
            return self.registers["B"]
        if operand == 6:
            return self.registers["C"]
        if operand == 7:
            raise ValueError("Invalid operand")

    def adv(self, operand): # Opcode 0
        operand = self.combo(operand)
        self.registers["A"] = self.registers["A"] // 2**operand # combo
        return self.registers["A"]

    def bxl(self, operand): # Opcode 1
        self.registers["B"] = self.registers["B"] ^ operand # literal
        return self.registers["B"]

    def bst(self, operand): # Opcode 2
        operand = self.combo(operand)
        self.registers["B"] = operand % 8 # combo
        return self.registers["B"]

    def jnz(self, operand): # Opcode 3
        if self.registers["A"] != 0:
            self.instruction_pointer = operand - 2 # literal
        return self.instruction_pointer

    def bxc(self, operand): # Opcode 4
        self.registers["B"] = self.registers["B"] ^ self.registers["C"] # no operand
        return self.registers["B"]

    def out(self, operand): # Opcode 5
        operand = self.combo(operand)
        c = operand % 8 # combo
        self.output.append(c)

        '''match_pointer = len(self.output) - 1

        if match_pointer >= len(self.program) or self.output[match_pointer] != self.program[match_pointer]:
            # print(self.output)
            raise Exception("Program and output don't match")'''
        return c

    def bdv(self, operand): # Opcode 6
        operand = self.combo(operand)
        self.registers["B"] = self.registers["A"] // 2**operand # combo
        return self.registers["B"]

    def cdv(self, operand): # Opcode 7
        operand = self.combo(operand)
        self.registers["C"] = self.registers["A"] // 2**operand # combo
        return self.registers["C"]

    def read_instruction(self):
        instruction = self.program[self.instruction_pointer]
        operand = self.program[self.instruction_pointer + 1]

        #print(instruction, operand)

        routines = {
            0: self.adv, 1: self.bxl, 2: self.bst, 3: self.jnz,
            4: self.bxc, 5: self.out, 6: self.bdv, 7: self.cdv
            }

        routines[instruction](operand)

        self.instruction_pointer += 2
        return self.instruction_pointer

    def execute(self, A=None):
        if A is not None:
            self.registers["A"] = A
        while self.instruction_pointer < len(self.program) - 1:
            self.read_instruction()
            #print(self.registers, self.output)
        return self.output

    def execute_corrupted(self):
        i = 0

        while i < 10**7:
            i += 1
            #print(i)
            self.registers["A"] = i
            self.registers["B"] = 0
            self.registers["C"] = 0
            self.output = []
            self.instruction_pointer = 0

            try:
                while self.instruction_pointer < len(self.program) - 1:
                    self.read_instruction()
                    #print(self.program, self.registers, self.output)
                if len(self.output) == len(self.program):
                    return i
            except Exception as e:
                continue
                #print(e)
                    
if __name__ == "__main__":   
    nums = [bin(n)[2:] for n in range(8)]
    c = ChronospatialComputer("input.txt")
    output = c.program

    for n in range(len(output) - 1):
        new_nums = []
        for i in range(8):
            # Try tacking on i to each num, add to new nums if works
            for num in nums:
                k = int(num, 2) * 8 + i
                computer = ChronospatialComputer("input.txt")
                computer.execute(A=k)
                if computer.output == output[-n-2:]:
                    print(k, bin(k)[2:], computer.output)
                    new_nums.append(bin(k)[2:])
        nums = sorted(new_nums[::])

print(sorted([int(num, 2) for num in nums]))