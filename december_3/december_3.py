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