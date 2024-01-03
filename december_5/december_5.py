import re


def main():
    
    with open('./december_5/input.txt', 'r') as f:

        maps = {
            0: [],
            1: [],
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: []
        }

        current_map = None
        for line in f:
            line = line.strip()
            if "seeds" in line:
                maps[0] = list(map(int, re.findall(r'\d+', line)))
            elif "seed-to-soil map:" in line:
                current_map = 1
            elif "soil-to-fertilizer map:" in line:
                current_map = 2
            elif "fertilizer-to-water map:" in line:
                current_map = 3
            elif "water-to-light map:" in line:
                current_map = 4
            elif "light-to-temperature map:" in line:
                current_map = 5
            elif "temperature-to-humidity map:" in line:
                current_map = 6
            elif "humidity-to-location map:" in line:
                current_map = 7
            else:
                if current_map:
                    nums = list(map(int, line.split()))
                    maps[current_map].append(nums) if len(nums) > 0 else None

    def find_location_recursive(current_n, next_key):
        # first check the range or return the same n
        for mapping in maps[next_key]:
            destination = mapping[0]
            source = mapping[1]
            range_ = mapping[2]

            if source <= current_n < source + range_:
                current_n = destination + (current_n - source)
                break

        
        # update the next key
        next_key += 1

        # if we have the location return the recursivity
        if next_key == 8:
            return current_n
        
        return find_location_recursive(current_n, next_key)

    """ PART 1 """
    locations = []
    for seed in maps[0]:
        location = find_location_recursive(seed, 1)
        locations.append(location)

    print(f"The lowest location is: {min(locations)}")

    """ PART 2 """
    # this version is really inneficient
    locations = []
    counter = 0
    while counter < len(maps[0]):
        print(f"{counter}/{len(maps[0])}")
        source = maps[0][counter]
        range_ = maps[0][counter + 1]
        for seed in range(source, source+range_):
            location = find_location_recursive(seed, 1)
            locations.append(location)
        counter += 2
    
    print(f"The lowest location is: {min(locations)}")





if __name__ == '__main__':
    main()