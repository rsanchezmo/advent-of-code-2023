import copy
from pprint import pprint
from collections import deque

def main():
    with open("./december_16/input.txt") as f:
        map = f.readlines()

    map = [list(x.strip()) for x in map]
    energized_map = copy.deepcopy(map)


    next_beam_poses = deque()
    if map[0][0] == '/':
        next_beam_poses.append((0, 0, 'N'))
    elif map[0][0] == '\\':
        next_beam_poses.append((0, 0, 'S'))
    elif map[0][0] == '-':
        next_beam_poses.append((0, 0, 'N'))
        next_beam_poses.append((0, 0, 'S'))
    else:
        next_beam_poses.append((0, 0, 'E'))

    """ Part 1 """
    def in_bounds(x, y):
        return x >= 0 and y >= 0 and x < len(map[0]) and y < len(map)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def propagate_beam(beam_pose):
        """ recursively propagate beam """

        x, y, direction = beam_pose

        # check if beam is out of bounds
        if not in_bounds(x, y):
            return
        
        energized_map[y][x] = "#"

        if direction == 'E':
            if not in_bounds(x + 1, y):
                return
            
            if map[y][x + 1] == '/':
                next_beam_poses.append((x + 1, y, 'N'))
            elif map[y][x + 1] == '\\':
                next_beam_poses.append((x + 1, y, 'S'))
            elif map[y][x + 1] == '|':
                next_beam_poses.append((x + 1, y, 'N'))
                next_beam_poses.append((x + 1, y, 'S'))
            else:
                next_beam_poses.append((x + 1, y, 'E'))
            return
            
        elif direction == 'N':
            if not in_bounds(x, y - 1):
                return
            
            if map[y - 1][x] == '/':
                next_beam_poses.append((x, y - 1, 'E'))
            elif map[y - 1][x] == '\\':
                next_beam_poses.append((x, y - 1, 'W'))
            elif map[y - 1][x] == '-':
                next_beam_poses.append((x, y - 1, 'E'))
                next_beam_poses.append((x, y - 1, 'W'))
            else:
                next_beam_poses.append((x, y - 1, 'N'))
            return

        elif direction == 'S':
            if not in_bounds(x, y + 1):
                return
            
            if map[y + 1][x] == '/':
                next_beam_poses.append((x, y + 1, 'W'))
            elif map[y + 1][x] == '\\':
                next_beam_poses.append((x, y + 1, 'E'))
            elif map[y + 1][x] == '-':
                next_beam_poses.append((x, y + 1, 'E'))
                next_beam_poses.append((x, y + 1, 'W'))
            else:
                next_beam_poses.append((x, y + 1, 'S'))
            return

        elif direction == 'W':
            if not in_bounds(x - 1, y):
                return
            
            if map[y][x - 1] == '/':
                next_beam_poses.append((x - 1, y, 'S'))
            elif map[y][x - 1] == '\\':
                next_beam_poses.append((x - 1, y, 'N'))
            elif map[y][x - 1] == '|':
                next_beam_poses.append((x - 1, y, 'N'))
                next_beam_poses.append((x - 1, y, 'S'))
            else:
                next_beam_poses.append((x - 1, y, 'W'))
            return

    while next_beam_poses:
        propagate_beam(next_beam_poses.popleft())

    print(f"Part 1: {sum([x.count('#') for x in energized_map])}")

    """ Part 2 """
    energizes = []

    # get initial points from top line
    for i in range(len(map[0])):
        next_beam_poses = deque()
        energized_map = copy.deepcopy(map)
        propagate_beam.cache_clear()

        if map[0][i] == '/':
            next_beam_poses.append((i, 0, 'W'))
        elif map[0][i] == '\\':
            next_beam_poses.append((i, 0, 'E'))
        elif map[0][i] == '-':
            next_beam_poses.append((i, 0, 'E'))
            next_beam_poses.append((i, 0, 'W'))
        else:
            next_beam_poses.append((i, 0, 'S'))

        while len(next_beam_poses) > 0:
            next_pose = next_beam_poses.popleft()
            propagate_beam(next_pose)

        energizes.append(sum([x.count('#') for x in energized_map]))

    # get initial points from bottom line
    for i in range(len(map[-1])):
        next_beam_poses = deque()
        energized_map = copy.deepcopy(map)
        propagate_beam.cache_clear()

        if map[-1][i] == '/':
            next_beam_poses.append((i, len(map) - 1, 'E'))
        elif map[-1][i] == '\\':
            next_beam_poses.append((i, len(map) - 1, 'W'))
        elif map[-1][i] == '-':
            next_beam_poses.append((i, len(map) - 1, 'E'))
            next_beam_poses.append((i, len(map) - 1, 'W'))
        else:
            next_beam_poses.append((i, len(map) - 1, 'N'))

        while next_beam_poses:
            propagate_beam(next_beam_poses.popleft())

        energizes.append(sum([x.count('#') for x in energized_map]))

    # get initial points from left line
    for i in range(len(map)):
        next_beam_poses = deque()
        energized_map = copy.deepcopy(map)
        propagate_beam.cache_clear()

        if map[i][0] == '/':
            next_beam_poses.append((0, i, 'N'))
        elif map[i][0] == '\\':
            next_beam_poses.append((0, i, 'S'))
        elif map[i][0] == '|':
            next_beam_poses.append((0, i, 'N'))
            next_beam_poses.append((0, i, 'S'))
        else:
            next_beam_poses.append((0, i, 'E'))

        while next_beam_poses:
            propagate_beam(next_beam_poses.popleft())

        energizes.append(sum([x.count('#') for x in energized_map]))

    # get initial points from right line
    for i in range(len(map)):
        next_beam_poses = deque()
        energized_map = copy.deepcopy(map)
        propagate_beam.cache_clear()

        if map[i][-1] == '/':
            next_beam_poses.append((len(map[0]) - 1, i, 'S'))
        elif map[i][-1] == '\\':
            next_beam_poses.append((len(map[0]) - 1, i, 'N'))
        elif map[i][-1] == '|':
            next_beam_poses.append((len(map[0]) - 1, i, 'N'))
            next_beam_poses.append((len(map[0]) - 1, i, 'S'))
        else:
            next_beam_poses.append((len(map[0]) - 1, i, 'W'))

        while next_beam_poses:
            propagate_beam(next_beam_poses.popleft())

        energizes.append(sum([x.count('#') for x in energized_map]))

    print(f"Part 2: {max(energizes)}")

if __name__ == "__main__":
    main()