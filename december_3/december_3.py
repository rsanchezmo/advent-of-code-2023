"""
--- Day 3: Gear Ratios ---
You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?


--- Part Two ---
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?

"""

import re

def check_around(engine, i_line, pos):
    x_limits = len(engine[0])
    y_limits = len(engine)

    for x in range(pos-1, pos+2):
        if x < 0 or x >= x_limits:
            continue
        for y in range(i_line-1, i_line+2):
            if y < 0 or y >= y_limits or (x == pos and y == i_line):
                continue
            if (not engine[y][x].isdigit()) and engine[y][x] != '.' and engine[y][x] != '\n':
                return True

    return False

def check_around_2(engine, i_line, pos, stars, num):
    x_limits = len(engine[0])
    y_limits = len(engine)

    for x in range(pos-1, pos+2):
        if x < 0 or x >= x_limits:
            continue
        for y in range(i_line-1, i_line+2):
            if y < 0 or y >= y_limits or (x == pos and y == i_line):
                continue
            if engine[y][x] == '*':
                if stars.get((y,x), None) is not None:
                    stars[(y, x)].append(num)
                else:
                    stars[(y, x)] = [num]

                return True

    return False

def main():
    with open('./december_3/input.txt', 'r') as f:
        engine = f.readlines()


    """ PART 1 """
    part_numbers = []
    for i, line in enumerate(engine):
        for number in re.finditer(r'\d+', line):
            init_pos = number.start()
            end_pos = number.end()
            num = int(line[init_pos:end_pos])
            is_part_number = False
            for pos in range(init_pos, end_pos):
                is_part_number = check_around(engine, i, pos)
                if is_part_number:
                    break
            if is_part_number:
                part_numbers.append(num)

    print(f'Part numbers sum is: {sum(part_numbers)}')
                

    """ PART 2 """
    stars = {}
    for i, line in enumerate(engine):
        for number in re.finditer(r'\d+', line):
            init_pos = number.start()
            end_pos = number.end()
            num = int(line[init_pos:end_pos])
            is_gear = False
            for pos in range(init_pos, end_pos):
                is_gear = check_around_2(engine, i, pos, stars, num)
                if is_gear:
                    break
    
    total_sum = 0
    for values in stars.values():
        if len(values) == 2:
            value = values[0] * values[1]
            total_sum += value

    print(f'Gear ratio sum is: {total_sum}')

    

if __name__ == '__main__':
    main()