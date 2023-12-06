from run import BaseSolution

class Solution(BaseSolution):
    bag_content = {
        'red': 12,
        'green': 13,
        'blue': 14,
    }

    def part1(self):
        possible_games = []

        with self.path.open() as f:
            for line in f:
                header, subsets = line.rstrip('\n').split(': ')
                if self.check_if_game_possible(subsets):
                    game_number = header.split(' ')[-1]
                    possible_games.append(game_number)

        return sum(list(map(int, possible_games)))

    def check_if_game_possible(self, subsets):
        subsets = subsets.split('; ')
        for subset in subsets:
            color_results = subset.split(', ')
            for color_result in color_results:
                number, color = color_result.split(' ')
                if int(number) > self.bag_content[color]:
                    return False

        return True

    def part2(self):
        result = 0
        with self.path.open() as f:
            for line in f:
                subsets = line.rstrip('\n').split(': ')[-1]
                occurrences = self.find_color_occurrences(subsets)
                set_power = 1
                for _, numbers in occurrences.items():
                    set_power *= max(numbers)
                result += set_power

        return result

    def find_color_occurrences(self, subsets):
        occurrences = {k: [] for k in ('red', 'green', 'blue')}
        subsets = subsets.split('; ')
        for subset in subsets:
            color_results = subset.split(', ')
            for color_result in color_results:
                number, color = color_result.split(' ')
                occurrences[color].append(int(number))

        return occurrences