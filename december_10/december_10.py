from collections import deque
import numpy as np

def valid_move(pos, direction, lines):
    if direction == "N" and pos[0] - 1 >= 0:
        # only valid moves are | and 7 and F
        if lines[pos[0] - 1][pos[1]] in ["|", "7", "F"]:
            return True
    elif direction == "S" and pos[0] + 1 < len(lines):
        # only valid moves are | and L and J
        if lines[pos[0] + 1][pos[1]] in ["|", "L", "J"]:
            return True
    elif direction == "E" and pos[1] + 1 < len(lines[0]):
        # only valid moves are - and 7 and J
        if lines[pos[0]][pos[1] + 1] in ["-", "7", "J"]:
            return True
    elif direction == "W" and pos[1] - 1 >= 0:
        # only valid moves are - and F and L
        if lines[pos[0]][pos[1] - 1] in ["-", "F", "L"]:
            return True
    return False

def get_next(pos, lines, map_seen, max_distance):
    if valid_move(pos, "N", lines):
        if map_seen[pos[0] - 1][pos[1]] == max_distance:
            return (pos[0] - 1, pos[1], 0)
    if valid_move(pos, "S", lines):
        if map_seen[pos[0] + 1][pos[1]] == max_distance:
            return (pos[0] + 1, pos[1], 0)
    if valid_move(pos, "E", lines):
        if map_seen[pos[0]][pos[1] + 1] == max_distance:
            return (pos[0], pos[1] + 1, 0)
    if valid_move(pos, "W", lines):
        if map_seen[pos[0]][pos[1] - 1] == max_distance:
            return (pos[0], pos[1] - 1, 0)
        
    return None

def move(pos, direction):
    if direction == "N":
        return (pos[0] - 1, pos[1], pos[2] + 1)
    elif direction == "S":
        return (pos[0] + 1, pos[1], pos[2] + 1)
    elif direction == "E":
        return (pos[0], pos[1] + 1, pos[2] + 1)
    elif direction == "W":
        return (pos[0], pos[1] - 1, pos[2] + 1)

def main():
    with open("./december_10/input.txt") as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]

    """ Part 1 """
    start_position = None
    for i, line in enumerate(lines):
        if "S" in line:
            start_position = (i, line.index("S"), 0)  # (row, col, distance)
            break

    queue = deque()
    queue.append(start_position)
    map_seen = np.zeros((len(lines), len(lines[0])), dtype=int) - 1
    transition_map = {}

    while queue:
        start = queue.popleft()
        for direction in ["N", "S", "E", "W"]:
            if not valid_move(start, direction, lines):
                continue
            new_pos = move(start, direction)
            if map_seen[new_pos[0]][new_pos[1]] == -1:
                transition_map[new_pos[0:2]] = start[0:2]
                queue.append(new_pos)
        map_seen[start[0]][start[1]] = start[2]
        

    print(f"Part 1: {np.max(map_seen)}")

    """ Part 2 """
    # we need to compute the path of the loop
    # we can backprop from the max distance point
    max_distance_orig = np.max(map_seen)
    max_distance_pos = np.where(map_seen == max_distance_orig)
    max_distance_pos = (max_distance_pos[0][0], max_distance_pos[1][0], 0)

    loop_left = []
    loop_left.append(max_distance_pos[0:2])
    loop_right = []
    loop_right.append(max_distance_pos[0:2])

    # we need to find the first neighbour that has the max_distance - 1 [2 ways to go]
    left = True
    for direction in ["N", "S", "E", "W"]:
        if not valid_move(max_distance_pos, direction, lines):
            continue
        new_pos = move(max_distance_pos, direction)
        if map_seen[new_pos[0]][new_pos[1]] == max_distance_orig - 1:
            if left:
                loop_left.append(new_pos[0:2])
                left = False
            else:
                loop_right.append(new_pos[0:2])
    
    # we need to backprop from the max_distance_orig - 1 using the transition_map
    cur_pos = transition_map[loop_left[-1]]
    while True:
        loop_left.append(cur_pos)
        cur_pos = transition_map[cur_pos]
        if cur_pos == start_position[0:2]:
            break

    cur_pos = transition_map[loop_right[-1]]
    while True:
        loop_right.append(cur_pos)
        cur_pos = transition_map[cur_pos]
        if cur_pos == start_position[0:2]:
            break

    loop = loop_left + [start_position[0:2]] + loop_right[::-1]

    def compute_area(points):
        return sum([row1 * col2 - row2 * col1 for (row1, col1), (row2, col2) in zip(points[1:], points)]) / 2.

    # I have seen that can use the shoelace formula to calculate the area of a polygon as we now the coordinates of the vertices
    area = compute_area(loop)

    # later can use the picks theorem to find the number of points inside the polygon given the area
    interior_points = int(abs(area) - 0.5 * (len(loop) - 1) + 1)

    print(f"Part 2: {interior_points}")

if __name__ == "__main__":
    main()