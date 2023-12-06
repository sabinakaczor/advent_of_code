from run import BaseSolution
import re
from functools import reduce


class Solution(BaseSolution):
    spelled_digits = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9',
    }

    def part1(self):
        self.first_digit_pattern = re.compile(r'(?P<digit>\d)')
        self.last_digit_pattern = re.compile(r'.*(?P<digit>\d)')
        total = 0

        with self.path.open() as f:
            calibration_values = [self.get_calibration_value(line) for line in f]
            total = sum(calibration_values)

        return total

    def part2(self):
        digit_group = r'(?P<digit>\d|{0})'.format('|'.join(self.spelled_digits))
        total = 0

        self.first_digit_pattern = re.compile(r'{0}'.format(digit_group))
        self.last_digit_pattern = re.compile(r'.*{0}'.format(digit_group))

        with self.path.open() as f:
            calibration_values = [self.get_calibration_value(line, True) for line in f]
            total = sum(calibration_values)

        return total

    def get_calibration_value(self, line, parse = False):
        first = re.search(self.first_digit_pattern, line).group('digit')
        last = re.search(self.last_digit_pattern, line).group('digit')
        if parse:
            return int(self.parse_digit(first) + self.parse_digit(last))
        else:
            return int(first + last)

    def parse_digit(self, digit):
        return self.spelled_digits.get(digit, digit)