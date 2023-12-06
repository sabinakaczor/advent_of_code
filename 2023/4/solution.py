from run import BaseSolution
import re

class Solution(BaseSolution):

    def part1(self):
        total = 0
        with self.path.open() as f:
            for line in f:
                number_lists = line.split(':')[-1]
                owned_winning_numbers_count = self.count_owned_winning_numbers(number_lists)

                if owned_winning_numbers_count:
                    total += 2 ** (owned_winning_numbers_count - 1)

        return total

    def part2(self):
        owned_cards = {}
        with self.path.open() as f:
            for line in f:
                header, number_lists = line.split(':')
                card_number = int(re.split(r'\s+', header)[-1])
                owned_cards[card_number] = owned_cards.get(card_number, 0) + 1
                factor = owned_cards[card_number]

                owned_winning_numbers_count = self.count_owned_winning_numbers(number_lists)
                for i in range(owned_winning_numbers_count):
                    won_card_number = card_number + i + 1
                    owned_cards[won_card_number] = owned_cards.get(won_card_number, 0) + factor

        return sum(owned_cards.values())

    def count_owned_winning_numbers(self, number_lists):
        winning_list, owned_list = number_lists.split('|')
        winning_list = re.split(r'\s+', winning_list.strip())
        owned_list = re.split(r'\s+', owned_list.strip())

        return len(set(owned_list) & set(winning_list))