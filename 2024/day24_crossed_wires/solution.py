class Gate:
    def __init__(self, gate_type, inputs, output):
        self.type = gate_type
        self.inputs = inputs
        self.output = output

    def __repr__(self):
        return(f"{self.inputs[0]} {self.type} {self.inputs[1]} -> {self.output}")

class CrossedWires:
    def __init__(self, filename):
        self.wires = {}
        self.gates = []
        self._read_input(filename)

    def _read_input(self, filename):
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

    def apply_gate(self, gate):
        print(gate)
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

if __name__ == "__main__":
    w = CrossedWires("input.txt")
    print(w.wires)
    w.find_outputs()

    for key in sorted(w.wires.keys()):
        print(f"{key}: {w.wires[key]}")

    print(w.get_number("z"))

