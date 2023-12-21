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

if __name__ == "__main__":
    main()