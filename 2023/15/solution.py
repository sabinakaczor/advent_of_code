from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        result = 0

        with self.path.open() as f:
            steps = f.read().strip().split(',')
            for step in steps:
                result += self.get_hash(step)

        return result

    def get_hash(self, value):
        current_value = 0
        for ch in value:
            current_value += ord(ch)
            current_value *= 17
            current_value = current_value % 256

        return current_value
