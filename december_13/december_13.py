import math
import copy


def search_horizontal(pattern, smug=None):
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
                if (smug is not None) and (smug <= 2 * symmetry_axis):
                    return symmetry_axis + 1
                
                if smug is None:
                    return symmetry_axis + 1
                
        else:
            found = True
            for i in range(symmetry_axis+1, len(pattern)):
                if pattern[i] != pattern[2 * symmetry_axis - i + 1]:
                    found = False
                    break
            if found:
                if (smug is not None) and (smug > 2 * symmetry_axis - len(pattern) + 1):
                    return symmetry_axis + 1
                
                if smug is None:
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
    # make the pattern a list of lists not tuples
    for i in range(len(pattern)):
        pattern[i] = list(pattern[i]) if not isinstance(pattern[i], list) else pattern[i]
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
                smug_candidates.append((new_pattern, i)) # GIVE THE POSITION OF THE SMUG
                new_pattern = copy.deepcopy(pattern)
                break
            # if len(comparison) == 0 and abs(i-j) == 1: # remove what could be a symmetry axis candidate
            #     line[0] = -1
            #     pattern[i] = line
            #     new_pattern = copy.deepcopy(pattern)

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
        #print(horizontal, vertical)
        summarize += horizontal*100 + vertical

    print(f"Part 1: {summarize}")
    
    
    """ part 2 """  
    summarize = 0
    for i, pattern in enumerate(patterns):
        #print_pattern(pattern, mode="ORIGINAL")
        candidates = fix_smug_horizontal(copy.deepcopy(pattern))
        horizontal = 0
        solutions = []
        for candidate in candidates:
            sol = search_horizontal(candidate[0], candidate[1])
            if sol > 0:
                horizontal = sol
                solutions.append(horizontal)
        if len(solutions) > 1:
            for sol in solutions:
                if sol > 1 and sol < len(pattern) - 1:
                    horizontal = sol
                    break
                
        vertical = 0
        pattern_ver = copy.deepcopy(list(zip(*pattern)))
        candidates = fix_smug_horizontal(pattern_ver)
        solutions = []
        for candidate in candidates:
            sol = search_horizontal(candidate[0], candidate[1])
            if sol > 0:
                vertical = sol
                solutions.append(vertical)
        if len(solutions) > 1:
            for sol in solutions:
                if sol > 1 and sol < len(pattern) - 1:
                    vertical = sol
                    break

        #print(f"H: {horizontal} - V: {vertical}")
        summarize += horizontal*100 + vertical

    print(f"Part 2: {summarize}")
    

if __name__ == "__main__":
    main()

