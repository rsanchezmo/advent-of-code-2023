from dataclasses import dataclass
from typing import Tuple, List, Optional
import copy
from pprint import pprint
import time
from functools import lru_cache
import heapq

@dataclass
class Node:
    pose: Tuple[int, int]
    distance: int
    g: int
    h: int
    height: int = 0
    parent: 'Node' = None
    direction: Optional[Tuple[int, int]] = None

    @property
    def f(self):
        return self.g + self.h
    
    def __hash__(self) -> int:
        return hash(self.pose)
    
    
    def __eq__(self, other: object) -> bool:
        return self.pose == other.pose
    
    def __lt__(self, other):
        return self.f < other.f
    
    def __str__(self) -> str:
        return f"Node: {self.pose}, distance: {self.distance}, g: {self.g}, h: {self.h}, height: {self.height}, direction: {self.direction}, parent: {self.parent.pose if self.parent else None}"

def main():
    with open('./december_17/test.txt', 'r') as f:
        map = f.readlines()

    map = [list(line.strip()) for line in map]
    visited_map = copy.deepcopy(map)
    path_map = copy.deepcopy(map)

    map_height = len(map)
    map_width = len(map[0])


    @lru_cache(maxsize=None)
    def heuristic(start: Tuple[int, int], goal: Tuple[int, int]) -> int:
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])
        # return 0
    

    def compute_g(current_node: Node, neighbor_node: Node) -> int:
        return current_node.g + neighbor_node.height


    def get_neighbors(node: Node, heightmap: List[List[int]]) -> List[Node]:
        neighbors = []
        # Movimientos: derecha, abajo, izquierda, arriba
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

        if node.direction:
            dx_last, dy_last = node.direction
            allowed_directions = directions
            allowed_directions.remove((-dx_last, -dy_last)) # remove going back
        else:
            allowed_directions = directions

        for dx, dy in allowed_directions:
            new_x, new_y = node.pose[0] + dx, node.pose[1] + dy

            if 0 <= new_x < map_width and 0 <= new_y < map_height:
                new_height = int(heightmap[new_y][new_x])

                # Calcular la nueva distancia
                if node.direction == (dx, dy):
                    new_distance = node.distance + 1
                else:
                    new_distance = 1

                # Crear un nuevo nodo si no se excede el límite de movimientos en la misma dirección
                if new_distance <= 3:
                    new_node = Node(pose=(new_x, new_y), distance=new_distance, g=0, h=heuristic(node.pose, goal.pose), height=new_height, parent=node, direction=(dx, dy))
                    new_node.g = compute_g(node, new_node)
                    neighbors.append(new_node)

        return neighbors

    start = Node(pose=(0, 0), distance=0, g=0, h=heuristic((0, 0), (len(map[0]) - 1, len(map) - 1)))
    goal = Node(pose=(len(map[0])-1, len(map)-1), distance=0, g=0, h=0)

    """ Part 1 """
    def a_star(start: Node, goal: Node) -> int:
        opened_nodes = []
        heapq.heappush(opened_nodes, (start.f, start))
        closed_nodes = set()

        while opened_nodes:
            _, current_node = heapq.heappop(opened_nodes)

            if current_node.pose == goal.pose:
                total_cost = current_node.g
                return total_cost

            closed_nodes.add(current_node)
            visited_map[current_node.pose[1]][current_node.pose[0]] = '#'

            for neighbor in get_neighbors(current_node, map):
                if neighbor not in closed_nodes:
                    heapq.heappush(opened_nodes, (neighbor.f, neighbor))

        return -1 

    t_init = time.time()
    heat_loss = a_star(start, goal)
    print(f"Time: {time.time() - t_init}s")

    pprint(visited_map)
    # print('\n')
    # print('\n')
    # pprint(map)

    print(f"Part 1: Heat loss of {heat_loss}")

    """ Part 2 """

if __name__ == '__main__':
    main()
    