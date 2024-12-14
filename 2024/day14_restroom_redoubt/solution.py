import time
from matplotlib import pyplot as plt
from matplotlib import animation

def read_input(filename):
    robots = []
    with open(filename) as file:
        for line in file:
            p, v = line.split(" ")
            px, py = p.strip("p=").split(",")
            vx, vy = v.strip("v=").split(",")
            p = (int(px), int(py))
            v = (int(vx), int(vy))
            robots.append([p, v])
    return robots

def move(robot, time, map_dimensions):
    x, y = map_dimensions
    px, py = robot[0]
    vx, vy = robot[1]

    px_new = (px + time * vx) % x
    py_new = (py + time * vy) % y

    return px_new, py_new

def display(pos, map_dimensions):
    for i in range(map_dimensions[1]):
        for j in range(map_dimensions[0]):
            if (j, i) in pos:
                print("*", end="")
            else:
                print(".", end="")
        print()    

def quadrant(map_dimensions, p):
    midx_one, midy_one = map_dimensions[0] // 2, map_dimensions[1] // 2
    midx_two, midy_two = (map_dimensions[0] + 1) // 2, (map_dimensions[1] + 1) // 2

    # for 11, 7: 5, 3, 6, 4
    # (0, 4) and (6, 10), (0, 2) and (4, 6)

    # print(p[0], midx_one, midx_two, p[1], midy_one, midy_two)

    if p[0] < midx_one and p[1] < midy_one:
        return 0
    elif p[0] < midx_one and p[1] >= midy_two:
        return 1
    elif p[0] >= midx_two and p[1] >= midy_two:
        return 2
    elif p[0] >= midx_two and p[1] < midy_one:
        return 3

def calculate_safety_factor(robots, time, map_dimensions):
    p_new = [move(robot, time, map_dimensions) for robot in robots]
    quadrants = [quadrant(map_dimensions, p) for p in p_new]

    print(quadrants)

    num_robots = [quadrants.count(0), quadrants.count(1), quadrants.count(2), quadrants.count(3)]
    return num_robots, num_robots[0] * num_robots[1] * num_robots[2] * num_robots[3]


if __name__ == '__main__':
    robots = read_input("input.txt")
    t = 100
    map_dimensions = (101, 103)

    # print(calculate_safety_factor(robots, t, map_dimensions))

    42

    pos = [move(robot, 0, map_dimensions) for robot in robots]

    fig, ax = plt.subplots()
    ax.set(xlabel="0")
    sc = ax.scatter([p[0] for p in pos], [p[1] for p in pos])

    def update(frame):
        pos = [move(robot, frame * 103 + 7973, map_dimensions) for robot in robots]
        sc.set_offsets(pos)
        ax.set(xlabel=str(frame * 103 + 7973))
        return sc

    ani = animation.FuncAnimation(fig=fig, func=update, frames=100, interval=5000)
    plt.show()