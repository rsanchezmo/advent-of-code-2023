from pprint import pprint
import time

class Brick:
    def __init__(self, left_pose, right_pose, id):
        self.left_pose = left_pose
        self.right_pose = right_pose
        self.id = id

    def __str__(self):
        return f'Brick {self.id}, L: {self.left_pose}, R: {self.right_pose}'

    def __repr__(self):
        return f'Brick {self.id}, L: {self.left_pose}, R: {self.right_pose}'

    def __eq__(self, __value: object) -> bool:
        # ccompare the id and the pose
        return self.id == __value.id and self.left_pose == __value.left_pose and self.right_pose == __value.right_pose

def main():
    with open('./december_22/input.txt') as f:
        lines = f.readlines()

    """
    PART 1:
        1. Get the bricks list
        2. Must simulate the fall dawnward of the bricks
        3. Check which brick can be desintegrated
    """
    bricks = []
    for line in lines:
        line = line.strip()
        splitted_line = line.split('~')
        x_left, y_left, z_left = map(int, splitted_line[0].split(','))
        x_right, y_right, z_right = map(int, splitted_line[1].split(','))
        bricks.append(Brick(left_pose=(x_left, y_left, z_left), right_pose=(x_right, y_right, z_right), id=len(bricks)))

    # pprint(bricks)

    # 2. simulate the fall dawnward of the bricks
    def simulate_falling(bricks):
        occupied_cells = set()
        moving = False
        for brick in bricks:
            for x in range(brick.left_pose[0], brick.right_pose[0] + 1):
                for y in range(brick.left_pose[1], brick.right_pose[1] + 1):
                    occupied_cells.add((x, y, brick.right_pose[2]))

        new_bricks_list = []
        for brick in bricks:
            occupied = False
            for x in range(brick.left_pose[0], brick.right_pose[0] + 1):
                for y in range(brick.left_pose[1], brick.right_pose[1] + 1):
                    if ((x, y, brick.left_pose[2] - 1) in occupied_cells) or (brick.left_pose[2] - 1 == 0):
                        occupied = True
                        break
                if occupied:
                    break
            if not occupied:
                moving = True
                new_bricks_list.append(Brick(left_pose=(brick.left_pose[0], brick.left_pose[1], brick.left_pose[2] - 1), right_pose=(brick.right_pose[0], brick.right_pose[1], brick.right_pose[2] - 1), id=brick.id))
            else:
                new_bricks_list.append(brick)
        return new_bricks_list, moving
    
    moving = True
    while moving:
        bricks, moving = simulate_falling(bricks)

    # now check for each brick if it can be desintegrated
    static_bricks = bricks.copy()
    desintregrable = 0
    for i in range(len(static_bricks)):
        # remove the brick from the list of bricks
        bricks_without_brick = static_bricks.copy()
        bricks_without_brick.pop(i)
        if not simulate_falling(bricks_without_brick)[1]:
            # print(f'Brick {i} can be desintegrated')
            desintregrable += 1

    print(f'Part 1: N: {desintregrable}')

    # PART 2
    init_time = time.time()
    desintregrable = 0
    for i in range(len(static_bricks)):
        # remove the brick from the list of bricks
        bricks_without_brick = static_bricks.copy()
        bricks_without_brick.pop(i)
        backup_bricks = bricks_without_brick.copy()

        moving = True
        while moving:
            bricks_without_brick, moving = simulate_falling(bricks_without_brick)
        
        # count the number of bricks fallen
        for brick, backup_brick in zip(bricks_without_brick, backup_bricks):
            if brick.left_pose != backup_brick.left_pose or brick.right_pose != backup_brick.right_pose:
                desintregrable += 1

    print(f'Time: {time.time() - init_time}s')
    print(f'Part 2: N: {desintregrable}')


                







if __name__ == '__main__':
    main()