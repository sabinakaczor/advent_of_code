from run import BaseSolution

TYPE_HIGH_CARD = 0
TYPE_ONE_PAIR = 1
TYPE_TWO_PAIR = 2
TYPE_THREE_OF_A_KIND = 3
TYPE_FULL_HOUSE = 4
TYPE_FOUR_OF_A_KIND = 5
TYPE_FIVE_OF_A_KIND = 6

TYPES = (
    TYPE_HIGH_CARD,
    TYPE_ONE_PAIR,
    TYPE_TWO_PAIR,
    TYPE_THREE_OF_A_KIND,
    TYPE_FULL_HOUSE,
    TYPE_FOUR_OF_A_KIND,
    TYPE_FIVE_OF_A_KIND,
)

STRENGTH_DICT = {
    'A': 14,
    'K': 13,
    'Q': 12,
    'J': 11,
    'T': 10,
    '9': 9,
    '8': 8,
    '7': 7,
    '6': 6,
    '5': 5,
    '4': 4,
    '3': 3,
    '2': 2,
}

class Solution(BaseSolution):

    def part1(self):
        hands_by_type = {t: [] for t in TYPES}
        with self.path.open() as f:
            for line in f:
                hand, bid = line.split(' ')
                hand_type = self.get_hand_type(hand)
                hands_by_type[hand_type].append({
                    'hand': hand,
                    'bid': int(bid)
                })

        result_list = self.sort_hands(hands_by_type)
        return sum([x*y for x, y in result_list])

    def get_hand_type(self, hand):
        card_occurrences = {}
        for card in hand:
            card_occurrences[card] = card_occurrences.get(card, 0) + 1
        occurrences = sorted(card_occurrences.values(), reverse=True)

        if occurrences == [1, 1, 1, 1, 1]:
            return TYPE_HIGH_CARD
        elif occurrences == [2, 1, 1, 1]:
            return TYPE_ONE_PAIR
        elif occurrences == [2, 2, 1]:
            return TYPE_TWO_PAIR
        elif occurrences == [3, 1, 1]:
            return TYPE_THREE_OF_A_KIND
        elif occurrences == [3, 2]:
            return TYPE_FULL_HOUSE
        elif occurrences == [4, 1]:
            return TYPE_FOUR_OF_A_KIND
        else:
            return TYPE_FIVE_OF_A_KIND

    def sort_hands(self, hands_by_type):
        bid_rank_list = []
        current_rank = 1
        for hand_type in sorted(hands_by_type):
            key_lambda = lambda x: [STRENGTH_DICT[card] for card in x['hand']]
            sorted_hands = sorted(hands_by_type[hand_type], key=key_lambda)
            for hand in sorted_hands:
                bid_rank_list.append([current_rank, hand['bid']])
                current_rank += 1

        return bid_rank_list

    def part2(self):
        return ''
