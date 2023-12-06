from run import BaseSolution
from functools import reduce
import re

class Solution(BaseSolution):

    def part1(self):
        results = []
        with self.path.open() as f:
            content = f.readlines()
            times = self.parse_row(content[0])
            records = self.parse_row(content[1])
            races_data = zip(times, records)
            for time, record in races_data:
                results.append(self.get_number_of_possibilities(time, record))

        return reduce((lambda x, y: x * y), results)

    def part2(self):
        with self.path.open() as f:
            content = f.readlines()
            time, record = self.parse_race_data(content)

        return self.get_number_of_possibilities(time, record)

    def parse_row(self, row):
        return [int(x) for x in re.split(r'\s+', row.strip())[1:]]

    def parse_race_data(self, content):
        race_data = []
        for row in content:
            numbers = re.split(r'\s+', row.strip())[1:]
            number = ''.join(numbers)
            race_data.append(int(number))

        return race_data

    def get_number_of_possibilities(self, time, record):
        start = int(record / time + 1)
        loss_count = start * 2

        for i in range(start, time // 2):
            distance = i * (time - i)
            if distance <= record:
                loss_count += 2
            else:
                break

        return time + 1 - loss_count

