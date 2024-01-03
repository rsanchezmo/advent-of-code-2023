from pprint import pprint

def main():
    with open('./december_11/input.txt') as f:
        lines = f.readlines()

    expand_rows = set()
    expand_cols = set()
    galaxies = []
    for i, line in enumerate(lines):
        line = line.strip()
        if line.count('#') == 0:
            expand_rows.add(i) # we should expand the universe by 2
        else:
            for col, char in enumerate(line):
                if char == '#':
                    galaxies.append((i, col, len(galaxies)+1)) # (row, col, id)

    # finde the expand cols
    for col in range(len(lines[0].strip())):
        if [line[col] for line in lines].count('#') == 0:
            expand_cols.add(col)

    """ part 1 """
    distances = []
    for i, galaxy in enumerate(galaxies):
        if i == len(galaxies) - 1:
            break
        for j in range(i+1, len(galaxies)):
            galaxy2 = galaxies[j]


            # calculate the distance between the two galaxies
            distance = abs(galaxy[0] - galaxy2[0]) + abs(galaxy[1] - galaxy2[1])

            # add the distance for the expanded rows and cols
            for row in range(galaxy[0], galaxy2[0]+1):
                if row in expand_rows:
                    distance += 1
            limits = (galaxy[1], galaxy2[1]) if galaxy[1] < galaxy2[1] else (galaxy2[1], galaxy[1])
            for col in range(limits[0], limits[1]+1):
                if col in expand_cols:
                    distance += 1

            distances.append(distance)

    print(f"Sum of distances: {sum(distances)}, between {len(distances)} pairs")

    """ part 2 """
    distances = []
    for i, galaxy in enumerate(galaxies):
        if i == len(galaxies) - 1:
            break
        for j in range(i+1, len(galaxies)):
            galaxy2 = galaxies[j]


            # calculate the distance between the two galaxies
            distance = abs(galaxy[0] - galaxy2[0]) + abs(galaxy[1] - galaxy2[1])

            # add the distance for the expanded rows and cols
            for row in range(galaxy[0], galaxy2[0]+1):
                if row in expand_rows:
                    distance += (int(1e6) - 1)
            limits = (galaxy[1], galaxy2[1]) if galaxy[1] < galaxy2[1] else (galaxy2[1], galaxy[1])
            for col in range(limits[0], limits[1]+1):
                if col in expand_cols:
                    distance += (int(1e6) - 1)

            distances.append(distance)
    
    print(f"Sum of distances: {sum(distances)}, between {len(distances)} pairs")

if __name__ == "__main__":
    main()