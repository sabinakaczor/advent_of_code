import numpy as np

from run import BaseSolution

class Hailstone:
    def __init__(self, position, velocity) -> None:
        self.position = [int(p) for p in position]
        self.velocity = [int(v) for v in velocity]
        self.x, self.y, self.z = self.position
        self.vx, self.vy, self.vz = self.velocity

class Solution(BaseSolution):

    def get_hailstones(self):
        hailstones = []
        with self.path.open() as f:
            for line in f:
                line = line.strip()
                position, velocity = [data.strip().split(', ') for data in line.split('@')]
                hailstone = Hailstone(position, velocity)
                hailstones.append(hailstone)

        return hailstones

    def part1(self):
        if self.is_test:
            self.range_from, self.range_to = 7, 27
        else:
            self.range_from, self.range_to = 200000000000000, 400000000000000

        hailstones = self.get_hailstones()
        return self.count_intersections(hailstones)


    def count_intersections(self, hailstones):
        intersections = 0
        for i, first in enumerate(hailstones):
            for second in hailstones[i+1:]:
                intersections += self.get_intersection_rate(first, second)

        return intersections

    def get_intersection_rate(self, first: Hailstone, second: Hailstone):
        t1_denominator = second.vx * first.vy - second.vy * first.vx
        t2_denominator = second.vx

        if not t1_denominator or not t2_denominator:
            return 0
        t1_numerator = second.vx * (second.y - first.y) + second.vy * (first.x - second.x)

        t1 = t1_numerator / t1_denominator

        t2_numerator = first.x - second.x + first.vx * t1
        t2 = t2_numerator / t2_denominator

        if t1 < 0 or t2 < 0:
            return 0

        intersection_x = first.x + first.vx * t1
        intersection_y = first.y + first.vy * t1

        return (intersection_x >= self.range_from and intersection_x <= self.range_to
            and intersection_y >= self.range_from and intersection_y <= self.range_to)

    def part2(self):
        hailstones = self.get_hailstones()
        x, dx, y = self.solve_two_dimensions_equations(hailstones)[:3]
        z = self.solve_third_dimension_equations(hailstones, x, dx)[0]

        return x + y + z

    def solve_two_dimensions_equations(self, hailstones):
        h0 = hailstones[0]

        coefficient_matrix = np.array([
            [
                h0.velocity[1] - hailstones[i].velocity[1],
                hailstones[i].position[1] - h0.position[1],
                hailstones[i].velocity[0] - h0.velocity[0],
                h0.position[0] - hailstones[i].position[0]
            ] for i in range(1, 5)
        ])
        ordinate_values = np.array([
            h0.velocity[1] * h0.position[0]
                - h0.velocity[0] * h0.position[1]
                + hailstones[i].velocity[0] * hailstones[i].position[1]
                - hailstones[i].velocity[1] * hailstones[i].position[0]
            for i in range(1, 5)])

        # [x, dx, y, _dy] is returned
        return [round(r) for r in np.linalg.solve(coefficient_matrix, ordinate_values)]

    def solve_third_dimension_equations(self, hailstones, x, dx):
        h0 = hailstones[0]
        h1 = hailstones[1]

        t1 = (h0.position[0] - x) / (dx - h0.velocity[0])
        t2 = (h1.position[0] - x) / (dx - h1.velocity[0])

        coefficient_matrix = np.array([
            [1, t1],
            [1, t2],
        ])
        ordinate_values = np.array([
            h0.position[2] + t1 * h0.velocity[2],
            h1.position[2] + t2 * h1.velocity[2]
        ])

        # [z, dz] is returned
        return [round(r) for r in np.linalg.solve(coefficient_matrix, ordinate_values)]

