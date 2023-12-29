from run import BaseSolution

LEFT_TO_RIGHT = (0, 1)
RIGHT_TO_LEFT = (0, -1)
UP_TO_DOWN = (1, 0)
DOWN_TO_UP = (-1, 0)

'''

mirror /

0,1 -> -1,0
0,-1 -> 1,0
1,0 -> 0,-1
-1,0 -> 0,1

mirror \

0,1 -> 1,0
0,-1 -> -1,0
1,0 -> 0,1
-1,0 -> 0,-1

'''


#

class PositionsIndex:

    def __init__(self):
        self.index = []
        self.visited = []

    def add_position(self, pos):
        if pos not in self.index:
            self.index.append(pos)

    def mark_as_visited(self, pos):
        self.visited.append(pos)

    def get_unvisited(self):
        return [pos for pos in self.index if pos not in self.visited]


class Solution(BaseSolution):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.energized_tiles = set()
        self.index = PositionsIndex()

    def part1(self):
        with self.path.open() as f:
            content = [line.strip() for line in f.readlines()]

        return self.simulate_beams(content)

    def simulate_beams(self, content):
        t = ((0, 0), LEFT_TO_RIGHT)
        self.index.add_position(t)

        unvisited = self.index.get_unvisited()
        while unvisited:
            beam_data = unvisited[0]
            self.process_pos(beam_data, content)
            unvisited = self.index.get_unvisited()

        return len(self.energized_tiles)

    def process_pos(self, beam_data, content):
        self.index.add_position(beam_data)
        self.index.mark_as_visited(beam_data)

        pos, direction = beam_data
        row, col = pos
        if row < 0 or col < 0 or row >= len(content) or col >= len(content[0]):
            return

        self.energized_tiles.add(pos)
        symbol = content[row][col]

        if symbol == '|' and direction in (LEFT_TO_RIGHT, RIGHT_TO_LEFT):
            self.index.add_position(((row - 1, col), DOWN_TO_UP))
            self.index.add_position(((row + 1, col), UP_TO_DOWN))
            return
        if symbol == '-' and direction in (UP_TO_DOWN, DOWN_TO_UP):
            self.index.add_position(((row, col - 1), RIGHT_TO_LEFT))
            self.index.add_position(((row, col + 1), LEFT_TO_RIGHT))
            return

        if symbol == '\\':
            direction = (direction[1], direction[0])
        elif symbol == '/':
            direction = (-1 * direction[1], -1 * direction[0])

        self.process_pos((tuple([a + b for a, b in zip(pos, direction)]), direction), content)
