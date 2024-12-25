from random import randint

class Gate:
    def __init__(self, gate_type, inputs, output):
        self.type = gate_type
        self.inputs = inputs
        self.output = output

    def __repr__(self):
        return(f"{self.inputs[0]} {self.type} {self.inputs[1]} -> {self.output}")

class CrossedWires:
    def __init__(self, filename=None, wires=None):
        self.wires = {}
        self.gates = []
        self._read_input(filename)

    def _read_input(self, filename, wires=None):
        with open(filename) as file:
            wires, gates = file.read().strip().split("\n\n")

            wires = wires.split("\n")
            gates = gates.split("\n")

            for wire in wires:
                name, value = wire.split(": ")
                self.wires[name] = int(value)

            for gate in gates:
                gate_split = gate.split(" ")
                inputs = [gate_split[0], gate_split[2]]
                gate_type = gate_split[1]
                output = gate_split[-1]

                for wire in inputs:
                    if wire not in self.wires:
                        self.wires[wire] = None

                if output not in self.wires:
                    self.wires[output] = None

                self.gates.append(Gate(gate_type, inputs, output))

        self.gates_dict = {}
        for gate in self.gates:
            self.gates_dict[gate.output] = gate

    def apply_gate(self, gate):
        #print(gate)
        operations_dict = {
            "AND": (lambda x, y: x & y),
            "OR": (lambda x, y: x | y),
            "XOR": (lambda x, y: x ^ y)
        }

        if self.wires[gate.inputs[0]] is not None and self.wires[gate.inputs[1]] is not None:
            out = operations_dict[gate.type](self.wires[gate.inputs[0]], self.wires[gate.inputs[1]])
            self.wires[gate.output] = out
            return None
        else:
            return list(filter(lambda x: self.wires[x] is None, gate.inputs))

    def find_outputs(self):
        gate_dict = {}
        for gate in self.gates:
            gate_dict[gate.output] = gate

        for key, val in self.wires.items():
            wire_stack = []
            if val is None:
                wire_stack.append(key)
            while wire_stack:
                result = self.apply_gate(gate_dict[wire_stack[-1]])
                if result is None:
                    wire_stack.pop()
                else:
                    wire_stack.extend(result)

    def get_number(self, ch):
        n = ""
        for wire in sorted(self.wires.keys()):
            if wire[0] == ch:
                n += str(self.wires[wire])
        return int(n[::-1], 2)

    def get_expression(self, wire):
        gate_dict = {}
        for gate in self.gates:
            gate_dict[gate.output] = gate

        wire_stack = [wire]
        s = wire

        while wire_stack:
            w = wire_stack.pop()

            if w in gate_dict:
                gate = gate_dict[w]
                s = s.replace(w, f"({gate.inputs[0]} {gate.type} {gate.inputs[1]})")
                wire_stack.extend(gate.inputs)

        return s

    def initialize(self, a, b):
        for wire in self.wires.keys():
            self.wires[wire] = None

        for i in range(45):
            x = a % 2
            y = b % 2
            a //= 2
            b //= 2

            self.wires["x" + str(i).zfill(2)] = x
            self.wires["y" + str(i).zfill(2)] = y


if __name__ == "__main__":
    w = CrossedWires("input.txt")
    w.find_outputs()