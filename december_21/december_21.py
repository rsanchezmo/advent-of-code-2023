from pprint import pprint
import time
from functools import lru_cache
from typing import Tuple
import copy

def main():
    with open("./december_21/input.txt") as f:
        lines = f.readlines()

    map_ = []
    for line in lines:
        map_.append(list(line.strip()))

        if 'S' in line:
            start = (line.index('S'), len(map_) - 1)


    MOVES = {
        'N': (0, -1),
        'S': (0, 1),
        'E': (1, 0),
        'W': (-1, 0),
    }

    current_branches = set()
    current_branches.add(start)

    init_time = time.time()
    for step in range(64):
        # process all branches and create a new set containing all new branches
        new_branches = set()
        for branch in current_branches:
            for move in MOVES.values():
                new_x = branch[0] + move[0]
                new_y = branch[1] + move[1]
                if new_x < 0 or new_x >= len(map_[0]) or new_y < 0 or new_y >= len(map_):
                    continue
                if map_[new_y][new_x] == '#':
                    continue
                new_branches.add((new_x, new_y))

        current_branches = new_branches

    print(f'Time: {time.time() - init_time}s')
    print(f'Part 1_: {len(new_branches)}')

    # Part 2
    # i think i can solve with only 
    # 1 map, and a counter for each position, same computing, but with a counter on each position

    @lru_cache(maxsize=None)
    def step_map(branch: Tuple[int, int]):
        new_branches = []
        for move in MOVES.values():
            new_x = branch[0] + move[0]
            new_y = branch[1] + move[1]
            new_map_id = 0, 0

            # loop around the map
            if new_x < 0:
                new_x = len(map_[0]) - 1
                new_orig_x = -1
            elif new_x >= len(map_[0]):
                new_x = 0
                new_orig_x = 1
            else:
                new_orig_x = 0
            
            new_map_id = new_orig_x, new_map_id[1]

            if new_y < 0:
                new_y = len(map_) - 1
                new_orig_y = 1
            elif new_y >= len(map_):
                new_y = 0
                new_orig_y = -1
            else:
                new_orig_y = 0
            
            new_map_id = new_map_id[0], new_orig_y

            # avoid walls
            if map_[new_y][new_x] == '#':
                continue

            new_branches.append((new_x, new_y, *new_map_id))

        return new_branches
    
    # PART 2 SOLUTION BY USING DAY 9 AS SEEN IN REDDIT
    def find_next_value(sequence):
        differences = []
        for i in range(1, len(sequence)):
            differences.append(sequence[i] - sequence[i - 1])

        if all(difference == 0 for difference in differences):
            return sequence[-1] + differences[-1]
        
        return find_next_value(differences) + sequence[-1]
    
    @lru_cache(maxsize=None)
    def get_new_map_id(map_id_prev: Tuple[int, int], map_id: Tuple[int, int]):
        new_x = map_id_prev[0] + map_id[0]
        new_y = map_id_prev[1] + map_id[1]
        return new_x, new_y
    
    def get_solution_part_2(n_cycles):
        """ this is a brute force solution, but it works """
        current_branches = set()
        current_branches.add((*start, 0, 0))
        current_branches_dict = {start: {(0, 0)}}
        for _ in range(n_cycles):
            new_branches = {}
            for branch, branch_set in current_branches_dict.items():
                for new_branch in step_map(branch):
                    x, y, map_id_new_x, map_id_new_y = new_branch
                    for map_id in branch_set:
                        map_id_new = get_new_map_id(map_id, (map_id_new_x, map_id_new_y))
                        if (x, y) not in new_branches:
                            new_branches[(x, y)] = set()
                        new_branches[(x, y)].add(map_id_new)         
            current_branches_dict = new_branches  
        return sum([len(branch_set) for branch_set in current_branches_dict.values()])
    
    # cycles 26501365 = 202300 * 131 + 65
    y = []
    x = []
    next_value = 0
    window_size = 4
    import numpy as np

    for i in range(window_size):
        y.append(get_solution_part_2(65 + 131*i))
        x.append(65 + 131*i)

    y = np.array(y)
    x = np.array(x)
    p = np.polyfit(x, y, 2)
    p = np.poly1d(p)
    next_value = round(p(26501365))

    print(f'Part 2: {next_value}')


if __name__ == "__main__":
    main()