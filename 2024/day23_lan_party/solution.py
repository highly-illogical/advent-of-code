class LANParty:
    def __init__(self, filename):
        self._read_input(filename)

    def _read_input(self, filename):
        with open(filename) as file:
            self.G = {}
            for line in file:
                a, b = line.strip("\n").split("-")
                if a not in self.G:
                    self.G[a] = [b]
                else:
                    self.G[a].append(b)
                if b not in self.G:
                    self.G[b] = [a]
                else:
                    self.G[b].append(a)

    def find_3(self):
        triplets = []
        for node1 in self.G.keys():
            for node2 in self.G.keys():
                if node2 in self.G[node1]:
                    for node3 in self.G.keys():
                        if node3 in self.G[node2] and node3 in self.G[node1]:
                            if node1[0] == 't' or node2[0] == 't' or node3[0] == 't':
                                triplets.append(tuple(sorted([node1, node2, node3])))
        print(set(triplets))
        return(len(set(triplets)))

if __name__ == "__main__":
    lp = LANParty("input.txt")
    print(lp.G)
    triplets = lp.find_3()
    print(triplets)            