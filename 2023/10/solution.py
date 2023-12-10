from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        pipes_map = []
        starting_pos = None
        with self.path.open() as f:
            for row, line in enumerate(f):
                line = list(line.strip())
                pipes_map.append(line)
                if 'S' in line:
                    starting_pos = [row, line.index('S')]

        return self.find_loop_length(pipes_map, starting_pos)

    def find_loop_length(self, pipes_map, starting_pos):
        current_pos = self.find_next_after_start(starting_pos, pipes_map)
        current_val = pipes_map[current_pos[0]][current_pos[1]]
        direction = [current_pos[i] - v for i, v in enumerate(starting_pos)]
        length = 1

        EAST_TO_WEST = [0, -1]
        WEST_TO_EAST= [0, 1]
        NORTH_TO_SOUTH= [1, 0]
        SOUTH_TO_NORTH= [-1, 0]

        directions = {
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

        while True:
            if current_val == 'S':
                return length // 2 if length % 2 == 0 else length // 2 + 1
            elif current_val in directions:
                direction = directions[current_val][str(direction)]

            length += 1
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
