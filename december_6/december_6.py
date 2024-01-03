import re
import math

def main():
    with open('./december_6/input.txt', 'r') as f:
        lines = f.readlines()

    times = list(map(int, re.findall(r'\d+', lines[0])))
    distances = list(map(int, re.findall(r'\d+', lines[1])))

    def get_distance(time_held, max_time):
        return time_held * (max_time - time_held)


    """ Part 1 """
    product = 1
    for max_time, max_distance in zip(times, distances):
        counter = 0
        for time_held in range(max_time//2 + 1):
            if get_distance(time_held, max_time) > max_distance:
                if time_held == (max_time//2) and max_time % 2 == 0:
                    counter += 1
                else:
                    counter += 2
        product *= counter if counter > 0 else 1

    print(f"Product: {product}")

    """ Part 2 """
    with open('./december_6/input.txt', 'r') as f:
        lines = f.readlines()

    times = int(lines[0].split('Time: ')[1].replace(" ", ""))
    distances = int(lines[1].split('Distance: ')[1].replace(" ", ""))

    counter = 0
    for time_held in range(times//2 + 1):
        if get_distance(time_held, times) > distances:
            if time_held == (times//2) and times % 2 == 0:
                counter += 1
            else:
                counter += 2

    print(f"Number of ways to beat the race: {counter}")

if __name__ == "__main__":
    main()