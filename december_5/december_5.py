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
    use_inneficient_version = False
    if use_inneficient_version:
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
    else:
        locations = []
        for i in range(0, len(maps[0]), 2):
            ranges = [(maps[0][i], maps[0][i] + maps[0][i+1])]
            results = []
            for i, key in enumerate(maps.keys()):
                if i == 0:
                    continue
                while ranges:
                    start_range, end_range = ranges.pop()
                    for destination, start_map, range_ in maps[key]:
                        end_map = start_map + range_
                        offset = destination - start_map
                        if end_map <= start_range or end_range <= start_map: # if the ranges are not overlapping
                            continue

                        if start_range < start_map:  # if should split the range [create a new one and add the old one to the results]
                            ranges.append((start_range, start_map))
                            start_range = start_map

                        if end_map < end_range:  # if should split the range [create a new one and add the old one to the results]
                            ranges.append((end_map, end_range))
                            end_range = end_map

                        results.append((start_range + offset, end_range + offset))
                        break
                    else:
                        results.append((start_range, end_range))

                ranges = results.copy()
                results = []
            locations += ranges
        print(f"[Part 2] The lowest location is: {min(loc[0] for loc in locations)}")

                        
            





if __name__ == '__main__':
    main()