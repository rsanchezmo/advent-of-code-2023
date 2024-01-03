def move_north(col, row, map):
    if row - 1 < 0:
        return

    if map[row-1][col] == '#' or map[row-1][col] == 'O':
        return

    map[row - 1][col] = 'O'
    map[row][col] = '.'  # clear the O from the previous line

    return move_north(col, row-1, map)

def move_west(col, row, map):
    if col - 1 < 0:
        return

    if map[row][col-1] == '#' or map[row][col-1] == 'O':
        return

    map[row][col-1] = 'O'
    map[row][col] = '.'  # clear the O from the previous line

    return move_west(col-1, row, map)

def move_east(col, row, map):
    if col + 1 >= len(map):
        return

    if map[row][col+1] == '#' or map[row][col+1] == 'O':
        return

    map[row][col+1] = 'O'
    map[row][col] = '.'  # clear the O from the previous line

    return move_east(col+1, row, map)

from functools import lru_cache

def to_file(map):
    with open("./december_14/map.txt", "w") as f:
        for line in map:
            f.write("".join(line) + "\n")
    

@lru_cache(maxsize=None)
def cycle(map):
    map = unhash_map(map)

    # first move north
    for y, line in enumerate(map):
        if y == 0:
            continue

        o_indexes = [i for i, x in enumerate(line) if x == 'O']
        
        for x in o_indexes:
            move_north(x, y, map)

    # then move west
    for y, line in enumerate(map):
        o_indexes = [i for i, x in enumerate(line) if x == 'O']
        
        for x in o_indexes:
            move_west(x, y, map)

    # then move south
    for y, line in enumerate(reversed(map)):
        if y == 0:
            continue

        o_indexes = [i for i, x in enumerate(line) if x == 'O']
        
        for x in o_indexes:
            # move north with the map inversed
            move_north(x, y, map[::-1])
            
    # then move east
    for y, line in enumerate(map):
        o_indexes = [i for i, x in enumerate(line) if x == 'O']
        
        for x in reversed(o_indexes):
            move_east(x, y, map)

    map = hash_map(map)
            
    return map

def hash_map(map):
    return ["".join(line) for line in map]

def unhash_map(map):
    return [list(line.strip()) for line in map]

def main():
    with open("./december_14/input.txt") as f:
        map = f.readlines()

    for y, line in enumerate(map):
        map[y] = list(line.strip())


    """ Part 1"""
    for y, line in enumerate(map):
        if y == 0:
            continue

        o_indexes = [i for i, x in enumerate(line) if x == 'O']
        
        for x in o_indexes:
            move_north(x, y, map)


    sum_ = 0
    for i, line in enumerate(map):
        o_count = sum([1 for component in line if component == 'O'])
        sum_ += o_count * (len(map) - i)

    print(sum_)

    """ Part 2 """
    # reset map
    with open("./december_14/input.txt") as f:
        original_map = f.readlines()


    list_of_maps = []
    t = 0
    map = original_map.copy()
    max_cycle = 1000000000
    while t < max_cycle:
        print(f"cycle {t}/{max_cycle-1}")
        map = cycle(tuple(map))

        if map in list_of_maps:
            # see how many cycles can be skipped
            idx = list_of_maps.index(map)
            cycle_length = len(list_of_maps) - idx
            n_cycles = int((max_cycle - idx)/cycle_length)
            t = n_cycles * cycle_length + idx 
            t += 1  # to move to the next step
            list_of_maps = []

        else:
            list_of_maps.append(map.copy())
            t += 1
                

    sum_ = 0
    for i, line in enumerate(map):
        o_count = sum([1 for component in line if component == 'O'])
        sum_ += o_count * (len(map) - i)

    print(sum_)
            

if __name__ == "__main__":
    main()