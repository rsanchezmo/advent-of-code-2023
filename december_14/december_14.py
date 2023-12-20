"""
--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

"""

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