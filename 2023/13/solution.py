from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        result = 0

        with self.path.open() as f:
            pattern = []
            for line in f:
                line = line.strip()
                if not line:
                    result += self.find_reflection_result(pattern)
                    pattern = []
                else:
                    pattern.append(line)

            return result + self.find_reflection_result(pattern)

    def find_reflection_result(self, pattern):
        horizontal_reflection = self.find_reflection(pattern)
        if horizontal_reflection:
            return horizontal_reflection * 100

        return self.find_reflection(list(zip(*pattern)))

    def find_reflection(self, item):
        item_half = len(item) // 2
        for i in range(1, len(item)):
            if i <= item_half:
                x = 0
                y = 2*i - 1
            else:
                x = 2*i - len(item)
                y = len(item) - 1
            top = item[x:i]
            bottom_reverted = item[y : i-1 : -1]

            if top == bottom_reverted:
                return i

        return 0
