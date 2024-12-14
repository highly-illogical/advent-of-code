from collections import deque

def read_input(filename):
    with open(filename) as file:
        garden = [line.strip("\n") for line in file]
        return garden

def bfs(garden, regions, i, j):
    plant = garden[i][j]
    queue = deque([(i, j)])
    area = 0

    while len(queue):
        i, j = queue.popleft()
        area = area + 1
        for neighbour in [[-1, 0], [1, 0], [0, -1], [0, 1]]: # y, x format -> [down, up, left, right]
            m = i + neighbour[0]
            n = j + neighbour[1]

            if 0 <= m < len(garden) and 0 <= n < len(garden[m]) and garden[m][n] == plant and regions[m][n] == 0:
                regions[m][n] = regions[i][j]
                queue.append((m, n))
    return area

def find_regions(garden):
    regions = [[0 for col in garden] for row in garden]
    
    r = 1
    areas = {}
    for i in range(len(garden)):
        for j in range(len(garden[i])):
            if regions[i][j] == 0:
                regions[i][j] = r
                areas[r] = bfs(garden, regions, i, j)
                r = r + 1

    return regions, areas

def add_to_dict(d, k, v):
    if k not in d:
        d[k] = v
    else:
        d[k] += v

def calculate_perimeter(regions):
    perimeters = {}

    for i in range(len(regions)):
        add_to_dict(perimeters, regions[i][0], 1) # left side
        add_to_dict(perimeters, regions[i][-1], 1) # right side

        for j in range(1, len(regions[i])):
            if regions[i][j-1] != regions[i][j]:
                add_to_dict(perimeters, regions[i][j-1], 1) # right side
                add_to_dict(perimeters, regions[i][j], 1) # left side

    for j in range(len(regions[0])):
        add_to_dict(perimeters, regions[0][j], 1) # top side
        add_to_dict(perimeters, regions[-1][j], 1) # bottom side

        for i in range(1, len(regions)):
            if regions[i-1][j] != regions[i][j]:
                add_to_dict(perimeters, regions[i-1][j], 1) # bottom side
                add_to_dict(perimeters, regions[i][j], 1) # top side

    return perimeters

def calculate_price(areas, factors):
    total = 0
    for key, value in areas.items():
        price = value * factors[key]
        total += price
        print(f'{key}: {value} * {factors[key]} = {price}')

    return total

def calculate_sides(regions):
    region_coords = {}

    for row in regions:
        for region in row:
            if region not in region_coords:
                region_coords[region] = {"start_i": [[] for col in regions[0]], "end_i": [[] for col in regions[0]], "start_j": [[] for row in regions], "end_j": [[] for row in regions]}

    for i in range(len(regions)):
        region_coords[regions[i][-1]]["end_j"][i].append(len(regions[i])-1) # Mark end point
        region_coords[regions[i][0]]["start_j"][i].append(0) # Mark start point
        
        for j in range(1, len(regions[i])):
            if regions[i][j-1] != regions[i][j]:
                region_coords[regions[i][j-1]]["end_j"][i].append(j-1) # Mark end point
                region_coords[regions[i][j]]["start_j"][i].append(j) # Mark start point

    for j in range(len(regions[0])):
        region_coords[regions[-1][j]]["end_i"][j].append(len(regions)-1) # Mark end point
        region_coords[regions[0][j]]["start_i"][j].append(0) # Mark start point
        
        for i in range(1, len(regions)):
            if regions[i-1][j] != regions[i][j]:
                region_coords[regions[i-1][j]]["end_i"][j].append(i-1) # Mark end point
                region_coords[regions[i][j]]["start_i"][j].append(i) # Mark start point

    print(region_coords)

    region_sides = {}

    for region in region_coords.keys():
        sides = 0

        for i in range(len(regions)):
            if i == 0:
                previous_start = []
                previous_end = []
            else:
                previous_start = region_coords[region]["start_j"][i-1]
                previous_end = region_coords[region]["end_j"][i-1]

            start = region_coords[region]["start_j"][i]
            end = region_coords[region]["end_j"][i]

            for s in start:
                if s not in previous_start:
                    sides = sides + 1

            for e in end:
                if e not in previous_end:
                    sides = sides + 1

        for j in range(len(regions[0])):
            if j == 0:
                previous_start = []
                previous_end = []
            else:
                previous_start = region_coords[region]["start_i"][j-1]
                previous_end = region_coords[region]["end_i"][j-1]

            start = region_coords[region]["start_i"][j]
            end = region_coords[region]["end_i"][j]

            for s in start:
                if s not in previous_start:
                    sides = sides + 1

            for e in end:
                if e not in previous_end:
                    sides = sides + 1

        region_sides[region] = sides

    return region_sides

if __name__ == '__main__':
    garden = read_input("input.txt")
    regions, areas = find_regions(garden)

    '''for row in garden:
        print("".join(col for col in row))

    print()'''

    for region in regions:
        print("".join(str(r) for r in region))

    # perimeters = calculate_perimeter(regions)
    sides = calculate_sides(regions)

    # print(calculate_price(areas, perimeters))
    print(calculate_price(areas, sides))