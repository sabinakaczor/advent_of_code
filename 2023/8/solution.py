from run import BaseSolution
from functools import reduce
import re

from modules.helpers import lowest_common_multiple

class Solution(BaseSolution):

    def part1(self):
        instructions, network_map = self.parse_input()
        steps = 0
        current_node = 'AAA'
        while current_node != 'ZZZ':
            for index in instructions:
                steps += 1
                current_node = network_map[current_node][index]
                if current_node == 'ZZZ':
                    return steps

    def part2(self):
        self.instructions, self.network_map = self.parse_input()
        current_nodes = [node for node in self.network_map if node[-1] == 'A']
        steps_list = []
        for node in current_nodes:
            steps_list.append(self.count_steps_for_node(node))
        return reduce(lowest_common_multiple, steps_list)

    def count_steps_for_node(self, node):
        steps = 0
        while node[-1] != 'Z':
            for index in self.instructions:
                steps += 1
                node = self.network_map[node][index]
                if node[-1] == 'Z':
                    return steps

    def parse_input(self):
        network_map = {}
        instructions = ''
        with self.path.open() as f:
            lines = f.readlines()
            instructions = lines[0].strip()
            pattern = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')
            for line in lines[2:]:
                m = re.match(pattern, line.strip())
                nodes = m.groups()
                network_map[nodes[0]] = {'L': nodes[1], 'R': nodes[2]}
        return instructions, network_map
