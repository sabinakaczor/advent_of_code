import pathlib

from run import BaseSolution

DIRECTIONS = {
    'D': [1, 0],
    'U': [-1, 0],
    'R': [0, 1],
    'L': [0, -1],
}

class Position:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def move(self, vector):
        self.x += vector[0]
        self.y += vector[1]

class Solution(BaseSolution):

    def part1(self):
        self.find_loop_points()

        self.interior = {r: [] for r in self.loop_points}
        result = 0
        for r, row in self.loop_points.items():
            current_direction = row[min(row)]
            found_intersections = 1
            for i in range(min(row), max(row) + 1):
                if i in row:
                    result += 1
                    if row[i] != current_direction:
                        found_intersections += 1
                        current_direction = row[i]
                elif found_intersections % 2 == 1:
                    self.interior[r].append(i)
                    result += 1

        # self.draw_loop()
        # self.draw_loop(True)

        return result

    def find_loop_points(self):
        current_pos = Position(0, 0)
        current_direction = 'D'
        loop_points = {}

        with self.path.open() as f:
            for line in f:
                direction, steps = line.strip().split(' ')[:2]
                if direction in ('D', 'U'):
                    current_direction = direction

                for _ in range(int(steps)):
                    if current_pos.x not in loop_points:
                        loop_points[current_pos.x] = {}
                    loop_points[current_pos.x][current_pos.y] = current_direction
                    current_pos.move(DIRECTIONS[direction])

        loop_points[current_pos.x][current_pos.y] = current_direction

        self.loop_points = loop_points

    def draw_loop(self, with_interior = False):
        dir_name = str(pathlib.Path(__file__).parent.resolve())
        full_path = '/'.join((dir_name, 'loop_with_interior.txt' if with_interior else 'loop.txt'))

        with open(full_path, 'w') as f:
            min_row = min(self.loop_points)
            max_row = max(self.loop_points)
            min_col = min([min(row) for row in self.loop_points.values()])
            max_col = max([max(row) for row in self.loop_points.values()])

            for row in range(min_row, max_row + 1):
                f.write(str(row) + ' ')
                for col in range(min_col, max_col + 1):
                    if col in self.loop_points[row]:
                        sign = self.loop_points[row][col]
                    elif with_interior and col in self.interior[row]:
                        sign = '#'
                    else:
                        sign = '.'
                    f.write(sign)
                f.write('\n')
