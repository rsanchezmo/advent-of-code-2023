from pprint import pprint


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

    for step in range(64):
        # process all branches and create a new set containing all new branches
        new_branches = set()
        for branch in current_branches:
            for move in MOVES.values():
                if branch[0] + move[0] < 0 or branch[0] + move[0] >= len(map_[0]):
                    continue
                if map_[branch[1] + move[1]][branch[0] + move[0]] == '#':
                    continue
                new_branches.add((branch[0] + move[0], branch[1] + move[1]))

        current_branches = new_branches

    print(f'Part 1_: {len(new_branches)}')

if __name__ == "__main__":
    main()