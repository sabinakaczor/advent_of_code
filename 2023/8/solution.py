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
        instructions, network_map = self.parse_input()
        current_nodes = [node for node in network_map if node[-1] == 'A']
        steps_list = []
        for node in current_nodes:
            steps_list.append(self.count_steps_for_node(node, instructions, network_map))
        return reduce(lowest_common_multiple, steps_list)

    def count_steps_for_node(self, node, instructions, network_map):
        steps = 0
        while node[-1] != 'Z':
            for index in instructions:
                steps += 1
                node = network_map[node][index]
                if node[-1] == 'Z':
                    return steps

    def parse_input(self):
        network_map = {}
        instructions = ''
        with self.path.open() as f:
            lines = f.readlines()
            instructions = [0 if ch == 'L' else 1 for ch in lines[0].strip()]
            pattern = re.compile(r'^(\w{3}) = \((\w{3}), (\w{3})\)$')
            for line in lines[2:]:
                m = re.match(pattern, line.strip())
                nodes = m.groups()
                network_map[nodes[0]] = nodes[1:]
        return instructions, network_map
