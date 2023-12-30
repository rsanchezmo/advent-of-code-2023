from dataclasses import dataclass
from typing import Tuple
from collections import deque
import time 
from collections import namedtuple

@dataclass
class Node:
    pose: Tuple[int, int]
    parent_pose: Tuple[int, int]
    cost: int
    path: set

    def __hash__(self):
        return hash((*self.pose, self.cost))

    def __eq__(self, other):
        return self.pose == other.pose

    def __repr__(self):
        return f'Node(pose={self.pose}, parent_pose={self.parent_pose}, cost={self.cost}, path={self.path})'


def main():
    with open('./december_23/input.txt') as f:
        lines = f.readlines()

    map_ = []
    start, goal = None, None
    for i, line in enumerate(lines):
        line = list(line.strip())
        map_.append(line)

        if i == 0:
            start = (line.index('.'), 1) # can ommit first line
        elif i == len(lines) - 1:
            goal = (line.index('.'), i)

    
    open_nodes = deque()
    closed_nodes = set()

    new_path = set()
    new_path.add((start[0], 0))
    open_nodes.append(Node(pose=start, parent_pose=(start[0], 0), cost=1, path=new_path))

    MOVES = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def get_next_nodes(current_node, map_, closed_nodes, open_nodes, ignore_slopes=False, closed_poses=None):
        next_poses = []

        for move in MOVES:
            next_pose = (current_node.pose[0] + move[0], current_node.pose[1] + move[1])

            if next_pose[0] < 0 or next_pose[0] >= len(map_[0]) or next_pose[1] < 0 or next_pose[1] >= len(map_):
                continue

            if next_pose != current_node.parent_pose and map_[next_pose[1]][next_pose[0]] != '#':
                if not ignore_slopes:
                    if map_[next_pose[1]][next_pose[0]] == '>' and move[0] == -1:
                        continue
                    if map_[next_pose[1]][next_pose[0]] == '<' and move[0] == 1:
                        continue
                    if map_[next_pose[1]][next_pose[0]] == '^' and move[1] == 1:
                        continue
                    if map_[next_pose[1]][next_pose[0]] == 'v' and move[1] == -1:
                        continue
                
                next_poses.append(next_pose)
            else:
                continue
            
            new_path = current_node.path.copy()
            new_path.add(current_node.pose)
            node = Node(pose=next_pose, parent_pose=current_node.pose, cost=current_node.cost + 1, path=new_path)

            # TODO: what to do here in part 2?
            if not ignore_slopes:
                if node in closed_nodes:
                    continue
            else:
                if node.pose in node.path:
                    continue

            open_nodes.append(node)

        return next_poses

    init_time = time.time()
    while open_nodes:
        current = open_nodes.popleft()
        closed_nodes.add(current)
        get_next_nodes(current, map_, closed_nodes, open_nodes)

    max_cost = max([node.cost for node in closed_nodes])
    print(f'Time: {time.time() - init_time}s')
    print(f'Part 1: {max_cost}')

    # Part 2
    open_nodes = deque()
    closed_nodes = set()
    closed_poses = set()

    new_path = set()
    new_path.add((start[0], 0))
    open_nodes.append(Node(pose=start, parent_pose=(start[0], 0), cost=1, path=new_path))

    init_time = time.time()
    counter = 0
    max_path = 0
    while open_nodes:
        current = open_nodes.popleft()
        if current.pose == goal:
            max_path = current.cost
            #print(f'Counter: {counter} - Max Path: {current.cost}')

        closed_nodes.add(current)
        closed_poses.add(current.pose)
        get_next_nodes(current, map_, closed_nodes, open_nodes, ignore_slopes=True, closed_poses=closed_poses)

    print(f'Time: {time.time() - init_time}s')
    print(f'Part 2: {max_path}')

if __name__ == '__main__':
    main()