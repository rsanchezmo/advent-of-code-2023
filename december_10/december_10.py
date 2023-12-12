"""
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?


--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

"""

from collections import deque
import numpy as np
from pprint import pprint
from scipy.ndimage import binary_fill_holes

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
    with open("./december_10/test.txt") as f:
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

    while queue:
        start = queue.popleft()
        for direction in ["N", "S", "E", "W"]:
            if not valid_move(start, direction, lines):
                continue
            new_pos = move(start, direction)
            if map_seen[new_pos[0]][new_pos[1]] == -1:
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
    loop_left.append(max_distance_pos)
    loop_right = []
    loop_right.append(max_distance_pos)

    # we need to find the first neighbour that has the max_distance - 1 [2 ways to go]
    left = True
    for direction in ["N", "S", "E", "W"]:
        if not valid_move(max_distance_pos, direction, lines):
            continue
        new_pos = move(max_distance_pos, direction)
        if map_seen[new_pos[0]][new_pos[1]] == max_distance_orig - 1:
            if left:
                loop_left.append(new_pos)
                left = False
            else:
                loop_right.append(new_pos)
            
    # left side till 0
    max_distance = max_distance_orig - 1
    max_distance_pos = loop_left[-1]
    while max_distance >= 0:
        max_distance -= 1
        # get the neighbour that has the max_distance - 1
        for direction in ["N", "S", "E", "W"]:
            if not valid_move(max_distance_pos, direction, lines):
                continue
            new_pos = move(max_distance_pos, direction)
            if map_seen[new_pos[0]][new_pos[1]] == max_distance:
                loop_left.append(new_pos)
                max_distance_pos = new_pos
                break

    loop_left.append(start_position)

    # right side till 0
    max_distance = max_distance_orig - 1
    max_distance_pos = loop_right[-1]
    while max_distance >= 0:
        max_distance -= 1
        # get the neighbour that has the max_distance - 1
        for direction in ["N", "S", "E", "W"]:
            if not valid_move(max_distance_pos, direction, lines):
                continue
            new_pos = move(max_distance_pos, direction)
            if map_seen[new_pos[0]][new_pos[1]] == max_distance:
                loop_right.append(new_pos)
                max_distance_pos = new_pos
                break

    # now reverse the right side and append it to the left side
    loop_right.reverse()
    loop = loop_left + loop_right

    def compute_area(points):
        return sum([row1 * col2 - row2 * col1 for (row1, col1, _), (row2, col2, _) in zip(points, points[1:])]) / 2.

    # I have seen that can use the shoelace formula to calculate the area of a polygon as we now the coordinates of the vertices
    area = compute_area(loop)

    # later can use the picks theorem to find the number of points inside the polygon given the area
    interior_points = int(abs(area) - 0.5 * (len(loop) - 1) + 1)

    print(f"Part 2: {interior_points}")

if __name__ == "__main__":
    main()