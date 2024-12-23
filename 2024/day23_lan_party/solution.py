class LANParty:
    def __init__(self, filename):
        self.connected_components = []
        self._read_input(filename)

    def _read_input(self, filename):
        with open(filename) as file:
            self.G = {}
            for line in file:
                a, b = line.strip("\n").split("-")
                self.connected_components.append((a, b))
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
        self.triplets = triplets
        return(len(set(triplets)))

    def next_connected(self):
        nplus1_connected = []

        for component in self.connected_components:
            connected_nodes = set(self.G[component[0]])
            for node in component:
                connected_nodes = connected_nodes.intersection(self.G[node])

            for cn in connected_nodes:
                nplus1_connected.append(tuple(sorted([*component, cn])))

        self.connected_components = set(nplus1_connected)

if __name__ == "__main__":
    lp = LANParty("input.txt")
    print(lp.G)
    
    while len(lp.connected_components) > 1:
        lp.next_connected()

    print(",".join(list(lp.connected_components)[0]))