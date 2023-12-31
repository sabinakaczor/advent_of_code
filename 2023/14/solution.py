from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        with self.path.open() as f:
            content = f.readlines()
            content = list(zip(*content))[:-1]

            return self.calculate_total_north_support_load(content)

    def part2(self):
        with self.path.open() as f:
            content = [l.strip() for l in f.readlines()]

            n = 1000000000
            loads = []

            while True:
                content = self.spin_cycle(content)
                load = self.calculate_total_load(content)
                loads.append(load)

                i = 0
                while True:
                    try:
                        index = loads.index(load, i, -1)
                        diff = len(loads) - 1 - index

                        if diff > 1 and loads[index - diff + 1: index + 1] == loads[index + 1:]:
                            non_recurring_count = index + 2
                            target_index = (n - non_recurring_count) % diff + (non_recurring_count - diff) - 1
                            return loads[target_index]

                        i = index + 1

                    except ValueError:
                        break

    def spin_cycle(self, items):
        for i in range(0, 4):
            items = list(zip(*items))
            items = self.tilt_platform(items, i < 2)

        return items

    def tilt_platform(self, items, rounded_first = False):
        new_aspect = []
        for item in items:
            parts = ''.join(item).split('#')
            new_item = []

            for part in parts:
                rounded_rocks_count = len([x for x in part if x == 'O'])
                empty_count = len(part) - rounded_rocks_count

                if rounded_first:
                    transformed_part = rounded_rocks_count * 'O' + empty_count * '.'
                else:
                    transformed_part =  empty_count * '.' + rounded_rocks_count * 'O'

                new_item.append(transformed_part + '#')

            new_aspect.append(''.join(new_item)[:-1])

        return new_aspect

    def calculate_total_load(self, content):
        result = 0

        row_load = len(content)
        for row in content:
            rounded_rocks_count = len([x for x in row if x == 'O'])
            result += rounded_rocks_count * row_load
            row_load -= 1

        return result

    def calculate_total_north_support_load(self, columns):
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
