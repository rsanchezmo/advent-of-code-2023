from pprint import pprint

DIRS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, -1),
    'D': (0, 1),
}


NUM_TO_DIR = {
    0: 'R',
    1: 'D',
    2: 'L',
    3: 'U',
}


def main():
    with open("./december_18/input.txt", 'r') as f:
        lines = f.readlines()

    def get_area(distance, direction, pose):
        new_pose = (pose[0] + DIRS[direction][0] * distance, pose[1] + DIRS[direction][1] * distance) # (x, y)
        contrib_area = pose[0] * new_pose[1] - pose[1] * new_pose[0]  # row1*col2 - row2*col1
        return contrib_area, new_pose
    
    pose = (0, 0) 
    area = 0
    path = [pose]
    sum_distances = 0
    for line in lines:
        list_line = line.strip().split(' ')
        direction = list_line[0]
        distance = int(list_line[1])
        rgb_color = list_line[2].replace('(', '').replace(')', '')
        contrib_area, pose = get_area(distance, direction, pose)
        path.append(pose)
        area += contrib_area
        sum_distances += distance

    area = int(abs(area) * 0.5 + sum_distances / 2 + 1)  # shoelace formula from day 10
    pprint("Part 1: The area is {}".format(area))

    # Part 2
    pose = (0, 0) 
    area = 0
    path = [pose]
    sum_distances = 0
    for line in lines:
        list_line = line.strip().split(' ')
        rgb_color = list_line[2].replace('(', '').replace(')', '')

        # first five digits or rgb hex encodes the distance:
        distance = int(rgb_color[1:6], 16) # hex to int
        # last digit encodes the direction [0, R], [1, D], [2, L], [3, U]
        direction = NUM_TO_DIR[int(rgb_color[-1])]

        contrib_area, pose = get_area(distance, direction, pose)
        path.append(pose)
        area += contrib_area
        sum_distances += distance

    area = int(abs(area) * 0.5 + sum_distances / 2 + 1)  # shoelace formula from day 10
    pprint("Part 1: The area is {}".format(area))
        

if __name__ == "__main__":
    main()
    