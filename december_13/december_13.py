"""
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

--- Part Two ---
You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?
"""

import math
import copy


def search_horizontal(pattern):
    """ search for a horizontal line of reflection """
    
    # find the symmetry axis candidates
    symmetry_axises = []
    for i in range(len(pattern)-1):
        if pattern[i] == pattern[i+1]:
            symmetry_axises.append(i)

    if symmetry_axises == []:
        return 0
    
    for symmetry_axis in symmetry_axises:
        # now see if the symmetry is displaced from the middle
        middle = math.floor(len(pattern)/2.)
        if symmetry_axis < middle:
            found = True
            for i in range(symmetry_axis):
                if pattern[i] != pattern[2 * symmetry_axis - i + 1]:
                    found = False
                    break
            if found:
                return symmetry_axis + 1
                
        else:
            found = True
            for i in range(symmetry_axis+1, len(pattern)):
                if pattern[i] != pattern[2 * symmetry_axis - i + 1]:
                    found = False
                    break
            if found:
                return symmetry_axis + 1

    return 0

def compare_lists(list1, list2):
    differences = []
    for i in range(len(list1)):
        if abs(list1[i] - list2[i]) > 0:
            differences.append((i))
    return differences

def fix_smug_horizontal(pattern):
    """ fix the smug in the pattern """
    # search for a similar horizontal line with a difference of 1 [smug: 1 OR 0]
    new_pattern = copy.deepcopy(pattern)
    n_smugs = 0
    smug_candidates = []
    for i in range(len(pattern)-1):
        line = list(new_pattern[i]) if not isinstance(pattern[i], list) else new_pattern[i]
        new_pattern[i] = line
        for j in range(i+1, len(pattern)):
            comparison = compare_lists(pattern[i], pattern[j])
            if len(comparison) == 1:  # meaning an smug
                line[comparison[0]] = pattern[j][comparison[0]]  # should care about being 1 or 0?
                new_pattern[i] = line
                # print(new_pattern)
                n_smugs += 1
                smug_candidates.append(new_pattern)
                new_pattern = copy.deepcopy(pattern)
                break

    return smug_candidates



def print_pattern(pattern, mode="HORIZONTAL"):
    print(f"Mode: {mode}")
    for line in pattern:
        print(line)



def main():
    with open("./december_13/input.txt", "r") as f:
        lines = f.readlines()

    patterns = []
    pattern = []

    for line in lines:        
        if line == "\n":
            # close the pattern, reset a new one and add to patterns
            patterns.append(pattern)
            pattern = []
        else:
            insert_line = line.strip().replace(".", "0").replace("#", "1")
            insert_line = list(map(int, insert_line))
            pattern.append(insert_line)

    patterns.append(pattern)  # add the last pattern


    """ part 1 """
    summarize = 0
    for pattern in patterns:
        horizontal = search_horizontal(pattern)
        vertical = search_horizontal(list(zip(*pattern)))
        print(horizontal, vertical)
        summarize += horizontal*100 + vertical

    print(f"Part 1: {summarize}")
    
    
    """ part 2 """  
    summarize = 0
    for i, pattern in enumerate(patterns):
        print(f"Pattern #: {i}")
        print_pattern(pattern, mode="ORIGINAL")
        candidates = fix_smug_horizontal(pattern)
        horizontal = 0
        for candidate in candidates:
            horizontal = search_horizontal(candidate)
            if horizontal > 0:
                print("FOUND PATTERN")
                print_pattern(candidate, mode='HORIZONTAL')
                
        vertical = 0
        pattern_ver = list(zip(*pattern))
        candidates = fix_smug_horizontal(pattern_ver)
        for candidate in candidates:
            vertical = search_horizontal(candidate)
            if vertical > 0:
                print("FOUND PATTERN")
                print_pattern(candidate, mode='VERTICAL')

        print(f"H: {horizontal} - V: {vertical}")
        summarize += horizontal*100 + vertical

    print(f"Part 2: {summarize}")
    

if __name__ == "__main__":
    main()

