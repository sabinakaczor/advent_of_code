from run import BaseSolution
import pathlib

EAST_TO_WEST = [0, -1]
WEST_TO_EAST= [0, 1]
NORTH_TO_SOUTH= [1, 0]
SOUTH_TO_NORTH= [-1, 0]

DIRECTIONS = {
    '7': {
        str(WEST_TO_EAST): NORTH_TO_SOUTH,
        str(SOUTH_TO_NORTH): EAST_TO_WEST,
    },
    'J': {
        str(WEST_TO_EAST): SOUTH_TO_NORTH,
        str(NORTH_TO_SOUTH): EAST_TO_WEST
    },
    'L': {
        str(NORTH_TO_SOUTH): WEST_TO_EAST,
        str(EAST_TO_WEST): SOUTH_TO_NORTH
    },
    'F': {
        str(SOUTH_TO_NORTH): WEST_TO_EAST,
        str(EAST_TO_WEST): NORTH_TO_SOUTH
    },
}

class Solution(BaseSolution):

    def parse_input(self):
        pipes_map = []
        starting_pos = None
        with self.path.open() as f:
            for row, line in enumerate(f):
                line = list(line.strip())
                pipes_map.append(line)
                if 'S' in line:
                    starting_pos = [row, line.index('S')]

        return pipes_map, starting_pos

    def part1(self):
        pipes_map, starting_pos = self.parse_input()

        return self.find_loop_length(pipes_map, starting_pos)

    def find_loop_length(self, pipes_map, starting_pos):
        current_pos = self.find_next_after_start(starting_pos, pipes_map)
        current_val = pipes_map[current_pos[0]][current_pos[1]]
        direction = [current_pos[i] - v for i, v in enumerate(starting_pos)]
        length = 1

        while True:
            if current_val == 'S':
                return length // 2 if length % 2 == 0 else length // 2 + 1
            elif current_val in DIRECTIONS:
                direction = DIRECTIONS[current_val][str(direction)]

            length += 1
            current_pos = [current_pos[i] + v for i, v in enumerate(direction)]
            current_val = pipes_map[current_pos[0]][current_pos[1]]

    def part2(self):
        pipes_map, starting_pos = self.parse_input()
        loop_rows_map, loop_cols_map, start_pos_equivalent = self.find_loop_points(pipes_map, starting_pos)
        pipes_map[starting_pos[0]][starting_pos[1]] = start_pos_equivalent
        result = 0

        for row, values in enumerate(pipes_map):
            loop_row = sorted(loop_rows_map[row])

            for col, _ in enumerate(values):
                loop_col = sorted(loop_cols_map[col])

                if col in loop_row:
                    continue

                coords_beyond_loop_borders = (len(loop_row) and col >= loop_row[0] and col <= loop_row[-1] and
                                        len(loop_col) and row >= loop_col[0] and row <= loop_col[-1])
                if not coords_beyond_loop_borders:
                    continue

                if self.point_is_enclosed(loop_row, pipes_map[row], col):
                    result += 1

        return result

    def point_is_enclosed(self, loop_row, pipes_row, col):
        found_intersections = 0
        for i in loop_row:
            if i > col:
                return found_intersections % 2 == 1

            loop_point = pipes_row[i]
            if loop_point == '|':
                found_intersections += 1
            elif loop_point in ('L', 'F'):
                pair_start = loop_point
            elif loop_point in ('7', 'J'):
                pair = pair_start + loop_point
                to_add = 2 if pair in ('LJ', 'F7') else 1
                found_intersections += to_add

    def draw_loop(self, loop_rows_map, pipes_map):
        dir_name = str(pathlib.Path(__file__).parent.resolve())
        full_path = '/'.join((dir_name, 'loop.txt'))
        with open(full_path, 'w') as f:
            for row, values in enumerate(pipes_map):
                for col, value in enumerate(values):
                    sign = value if col in loop_rows_map[row] else ' '
                    f.write(sign)
                f.write('\n')

    def find_loop_points(self, pipes_map, starting_pos):
        rows_map = {r: [] for r in range(0, len(pipes_map))}
        cols_map = {c: [] for c in range(0, len(pipes_map[0]))}
        rows_map[starting_pos[0]].append(starting_pos[1])
        cols_map[starting_pos[1]].append(starting_pos[0])
        current_pos = self.find_next_after_start(starting_pos, pipes_map)
        current_val = pipes_map[current_pos[0]][current_pos[1]]
        direction = [current_pos[i] - v for i, v in enumerate(starting_pos)]

        while True:
            if current_val == 'S':
                start_pos_equivalent = '|' if direction[1] == 0 else '-'
                return rows_map, cols_map, start_pos_equivalent
            elif current_val in DIRECTIONS:
                direction = DIRECTIONS[current_val][str(direction)]

            rows_map[current_pos[0]].append(current_pos[1])
            cols_map[current_pos[1]].append(current_pos[0])
            current_pos = [current_pos[i] + v for i, v in enumerate(direction)]
            current_val = pipes_map[current_pos[0]][current_pos[1]]

    def find_next_after_start(self, starting_pos, pipes_map):
        max_row = len(pipes_map) - 1
        max_col = len(pipes_map[0]) - 1
        directions_to_check = [
            # go north
            {
                'direction': [-1, 0],
                'pipes': ['|', '7', 'F']
            },
            # go east
            {
                'direction': [0, 1],
                'pipes': ['-', '7', 'J']
            },
            # go south
            {
                'direction': [1, 0],
                'pipes': ['|', 'L', 'J']
            },
            # go west
            {
                'direction': [0, -1],
                'pipes': ['-', 'L', 'F']
            },
        ]

        for dir_to_check in directions_to_check:
            pos_to_check = [starting_pos[i] + v for i, v in enumerate(dir_to_check['direction'])]

            # if position is beyond the map, continue
            if pos_to_check[0] < 0 or pos_to_check[0] > max_row or pos_to_check[1] < 0 or pos_to_check[1] > max_col:
                continue

            checked_pos_value = pipes_map[pos_to_check[0]][pos_to_check[1]]

            if checked_pos_value in dir_to_check['pipes']:
                return pos_to_check
