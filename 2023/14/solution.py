from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        with self.path.open() as f:
            content = f.readlines()
            content = list(zip(*content))[:-1]

            return self.calculate_total_load(content)

    def calculate_total_load(self, columns):
        result = 0

        for col in columns:
            col_length = len(col)
            parts = ''.join(col).split('#')

            processed_count = 0
            for part in parts:
                rounded_rocks_count = len([x for x in part if x == 'O'])
                if rounded_rocks_count:
                    first = col_length - processed_count
                    last = first - rounded_rocks_count + 1
                    sequence_sum = (first + last) / 2 * rounded_rocks_count
                    result += sequence_sum

                processed_count += len(part) + 1

        return int(result)