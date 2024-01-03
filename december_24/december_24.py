from functools import lru_cache
from dataclasses import dataclass
from typing import Tuple
import sympy as sp
import time


@dataclass
class Hailstone:
    initial_pose: Tuple[int, int]
    velocity: Tuple[int, int]

    @property
    def slope(self):
        return self.velocity[1] / self.velocity[0]
    
    @property
    def intercept(self):
        return self.initial_pose[1] - self.slope * self.initial_pose[0]
    
    def is_past(self, x, y):
        # compute time
        return (x - self.initial_pose[0]) / self.velocity[0] < 0 or (y - self.initial_pose[1]) / self.velocity[1] < 0
    
    def get_value(self, x):
        return self.slope * x + self.intercept
    
    def __hash__(self) -> int:
        return hash((self.initial_pose, self.velocity))
    
    def __eq__(self, o: object) -> bool:
        return self.initial_pose == o.initial_pose and self.velocity == o.velocity
    
    def __str__(self) -> str:
        return f'({self.initial_pose[0]}, {self.initial_pose[1]}) @ ({self.velocity[0]}, {self.velocity[1]})'
    
def main():
    test = False
    filename = 'test.txt' if test else 'input.txt'
    with open(f'./december_24/{filename}') as f:
        lines = f.readlines()

    MIN = 200000000000000 if not test else 7
    MAX = 400000000000000 if not test else 24

    hailstones = []
    for line in lines:
        # px py pz @ vx vy vz (nanoseconds)
        line_split = line.strip().split(' @ ')
        x, y, z = map(int, line_split[0].split(', '))
        vx, vy, vz = map(int, line_split[1].split(', '))
        hailstones.append(Hailstone(initial_pose=(x, y, z), velocity=(vx, vy, vz)))


    @lru_cache(maxsize=None)
    def will_collide(h1, h2):
        # h1.slope * x + h1.intercept = h2.slope * x + h2.intercept

        if h1.slope == h2.slope:
            return False, None, "parallel lines"  # parallel lines

        x = (h2.intercept - h1.intercept) / (h1.slope - h2.slope)
        y = h1.get_value(x)
        if h1.is_past(x, y) or h2.is_past(x, y):
            return False, None, "past collission" # collision in the past
        if (MIN <= x <= MAX) and (MIN <= y <= MAX):
            return True, (x, y), "collision"
        return False, (x, y), "collision out of bounds"

    init_time = time.time()
    count_collisions = 0
    collissions = []
    for i in range(len(hailstones)):
        for j in range(i+1, len(hailstones)):
            collides, intersection, info = will_collide(hailstones[i], hailstones[j])
            # print(f'Collision {collides}: {hailstones[i]} {hailstones[j]} in {intersection} [{info}], {i} {j}')

            if collides:
                collissions.append((i, j))
                count_collisions += 1

    print(f"Time: {time.time() - init_time}s")
    print(f'Part 1: {count_collisions}')

    # Part 2
    # Can use the first 3 hailstones to find the 9 variables of the system (x,y,z,vx,vy,vz,t0,t1,t2) of equations as each hailstone gives 3 equations
    unknowns = sp.symbols('x y z dx dy dz t1 t2 t3')
    x, y, z, dx, dy, dz, t1, t2, t3 = unknowns

    equations = []
    for i, hailstone in enumerate(hailstones[:3]):
        equations.append(sp.Eq(x + unknowns[-i-1]*dx, hailstone.initial_pose[0] + unknowns[-i-1]*hailstone.velocity[0]))
        equations.append(sp.Eq(y + unknowns[-i-1]*dy, hailstone.initial_pose[1] + unknowns[-i-1]*hailstone.velocity[1]))
        equations.append(sp.Eq(z + unknowns[-i-1]*dz, hailstone.initial_pose[2] + unknowns[-i-1]*hailstone.velocity[2]))

    init_time = time.time()
    solution = sp.solve(equations, unknowns).pop()
    print(f"Time: {time.time() - init_time}s")    
    print(f'Part 2: {sum(solution[:3])}')

if __name__ == '__main__':
    main()  