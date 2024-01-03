from functools import lru_cache

@lru_cache(maxsize=None)
def num_solutions(first_part, second_part, group_count=0):
    """
    first_part: how many chars are left to be seen
    second_part: how many gropus are left to be seen
    group_count: how many components of the current group are seen so far
    """
    if not first_part:  # this returns 1 if we have a valid combination, else 0
        if not second_part and not group_count:
            # this case means we have no more second_part left and we have closed the last group
            return 1
        return 0
    
    solutions = 0

    if len(first_part) < sum(second_part) - group_count:
        # this means we have more groups than we have chars to fill them
        return 0

    if first_part[0] == '?':
        """ put a '.' """
        if group_count: # we were inside a group
            if second_part and second_part[0] == group_count: # we have closed a group, so remove the group from second_part and move to the next char
                solutions += num_solutions(first_part[1:], second_part[1:])
        else:
            solutions += num_solutions(first_part[1:], second_part) # it means we are not inside a group, so move on

        """ put a '#' """
        solutions += num_solutions(first_part[1:], second_part, group_count + 1) # it means we are extending the current group

    elif first_part[0] == '#':
        solutions += num_solutions(first_part[1:], second_part, group_count + 1) # it means we are extending the current group
    else:
        """ have a '.' """
        if group_count: # we were inside a group
            if second_part and second_part[0] == group_count: # we have closed a group, so remove the group from second_part and move to the next char
                solutions += num_solutions(first_part[1:], second_part[1:])
        else:
            solutions += num_solutions(first_part[1:], second_part) # it means we are not inside a group, so move on

    return solutions  # this returns the total number of combinations



def main():
    with open('./december_12/input.txt') as f:
        lines = f.readlines()


    """ Part 1 """
    total_count = 0
    for line in lines:
        line = line.strip()
        first_part = line.split(' ')[0]
        second_part = line.split(' ')[1]
        second_part = tuple([int(damaged_count) for damaged_count in second_part.split(',')]) # convert to tuple to be hashable for lru_cache

        total_count += num_solutions(first_part + '.', second_part) # add a '.' at the end to close the last group

    print(f"SUM of total possible solutions: {total_count}")

    """ Part 2 """
    total_count = 0
    for i, line in enumerate(lines):
        line = line.strip()
        first_part = line.split(' ')[0]
        second_part = line.split(' ')[1]
        second_part = tuple([int(damaged_count) for damaged_count in second_part.split(',')]) # convert to tuple to be hashable for lru_cache

        total_count += num_solutions('?'.join([first_part] * 5) + '.', second_part * 5)
            
    print(f"SUM of total possible solutions: {total_count}")
    

if __name__ == "__main__":
    main()
