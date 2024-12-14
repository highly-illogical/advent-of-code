def read_input(filename: str) -> list[list[str]]:
    with open(filename) as file:
        return [list(line.strip("\n")) for line in file]

def gcd(a, b): 
    if (a > b):
        if a % b > 0:
            return gcd(b, a % b)
        else:
            return b
    else:
        if b % a > 0:
            return gcd(a, b % a)
        else:
            return a


def antenna_locations(antenna_map: list[list[str]]) -> dict[str, list[tuple[int, int]]]:
    antennas = {}
    for i in range(len(antenna_map)):
        for j in range(len(antenna_map[i])):
            if antenna_map[i][j] != ".":
                if antenna_map[i][j] not in antennas:
                    antennas[antenna_map[i][j]] = [(i, j)]
                else:
                    antennas[antenna_map[i][j]].append((i, j))
    return antennas

def get_antinodes(antennas: list[tuple[int, int]], map_dimensions: tuple[int, int]) -> list[tuple[int, int]]:
    antinodes = []
    for i in range(len(antennas)):
        for j in range(i+1, len(antennas)):
            # Calculate the antinodes for the pair of antennas
            dy, dx = antennas[i][0] - antennas[j][0], antennas[i][1] - antennas[j][1]
            antinodes_pair = [(antennas[i][0] + dy, antennas[i][1] + dx), (antennas[j][0] - dy, antennas[j][1] - dx)]
            print(antennas[i], antennas[j], dy, dx, antinodes_pair)
            # Check if within bounds of map
            for an in antinodes_pair:
                if an[0] in range(map_dimensions[0]) and an[1] in range(map_dimensions[1]):
                    antinodes.append((an[0], an[1]))
    return list(set(antinodes))

def get_antinodes_two(antennas: list[tuple[int, int]], map_dimensions: tuple[int, int]) -> list[tuple[int, int]]:
    antinodes = []
    for i in range(len(antennas)):
        for j in range(i+1, len(antennas)):
            # Calculate the antinodes for the pair of antennas
            antinodes.extend(get_antinodes_for_pair_two(antennas[i], antennas[j], map_dimensions))
    return list(set(antinodes))

def get_antinodes_for_pair_two(c1, c2, map_dimensions):
    dy, dx = list(p - q for p, q in zip(c1, c2))
    d = gcd(abs(dy), abs(dx))
    dy, dx = dy // d, dx // d

    antinodes = []

    y, x = c1
    while 0 <= y < map_dimensions[0] and 0 <= x < map_dimensions[1]:
        antinodes.append((y, x))
        y = y + dy
        x = x + dx

    y, x = c1
    while 0 <= y < map_dimensions[0] and 0 <= x < map_dimensions[1]:
        antinodes.append((y, x))
        y = y - dy
        x = x - dx

    return list(set(antinodes))

def get_antinodes_for_map(antenna_map):
    map_dimensions = (len(antenna_map), len(antenna_map[0]))
    locations = antenna_locations(antenna_map)

    antinodes = []

    for antenna_type, coordinates in locations.items():
        antinodes.extend(get_antinodes_two(coordinates, map_dimensions))

    return(len(list(set(antinodes))), list(set(antinodes)))

def show_antinodes_on_map(antenna_map):
    antinodes = get_antinodes_for_map(antenna_map)
    print(antinodes[0])
    for an in antinodes[1]:
        antenna_map[an[0]][an[1]] = '#'
    for row in antenna_map:
        print("".join(row))

if __name__ == '__main__':
    antenna_map = read_input("input.txt")
    map_dimensions = (len(antenna_map), len(antenna_map[0]))
    locations = antenna_locations(antenna_map)

    print(show_antinodes_on_map(antenna_map))