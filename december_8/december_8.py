import itertools
import math
from functools import reduce


def main():
    
    with open("december_8/input.txt") as f:
        lines = f.readlines()

    orders = lines[0].strip()
    
    map = {}
    for line in lines[1:]:
        if line == "\n":
            continue

        map[line[0:3]] = (line[7:10], line[12:15])

    """ part 1 """
    current_position = "AAA"
    n_steps = 0
    for order in itertools.cycle(orders):
        current_position = map[current_position][0 if order == "L" else 1]
        n_steps += 1
        if current_position == "ZZZ":
            break

    print(f"It took {n_steps} steps to reach ZZZ.")


    """ part 2 """
    current_nodes = [node for node in map.keys() if node.endswith("A")]
    n_steps = [0] * len(current_nodes)
    for i, node in enumerate(current_nodes):
            current_position = node
            print(f"Initial position {current_position}")
            for order in itertools.cycle(orders):
                current_position = map[current_position][0 if order == "L" else 1]
                n_steps[i] += 1
                if current_position.endswith("Z"):
                    print(f"Reached Z at {current_position} in {n_steps[i]} steps.")
                    break

    def mcm(a, b):
        return abs(a*b) // math.gcd(a, b)

    def mcm_list(numeros):  # as I am using python 3.8, I cant use math.lcm
        return reduce(mcm, numeros)
    
    print(f"It took {mcm_list(n_steps)} steps to reach.")
        

if __name__ == "__main__":
    main()