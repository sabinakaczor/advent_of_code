from functools import reduce
import sys

sys.path.append('.')

from modules.helpers import divide_chunks

class PacketParser:
    def __init__(self, string_to_parse) -> None:
        if string_to_parse[0] == '[' and string_to_parse[len(string_to_parse)-1] == ']':
            string_to_parse = string_to_parse[1:-1]
        self.string_to_parse = string_to_parse
        
    def parse(self) -> list:
        self.result_packet = []
        self.number_to_append = ''
        self.packet_to_append = ''
        self.opening_count = self.closing_count = 0
        for s in self.string_to_parse:
            self.parse_character(s)
            
        if self.number_to_append:
            self.append_number()
        elif self.packet_to_append and self.opening_count == self.closing_count:
            self.append_packet()
            
        return self.result_packet
        
    def parse_character(self, s):
        if s == '[':
            self.parse_opening_bracket()
        elif s == ']':
            self.parse_closing_bracket()
        elif s == ',':
            self.parse_comma()
        else:
            self.parse_other(s)
    
    def parse_opening_bracket(self):
        self.opening_count += 1
        self.packet_to_append += '['
    
    def parse_closing_bracket(self):
        self.closing_count += 1
        self.packet_to_append += ']'
        
    def parse_comma(self):        
        if self.number_to_append:
            self.append_number()
        elif self.packet_to_append and self.opening_count == self.closing_count:
            self.append_packet()
        else:
            self.packet_to_append += ','
    
    def parse_other(self, s):        
        if self.opening_count:
            self.packet_to_append += s
        else:
            self.number_to_append += s
            
    def append_number(self):
        self.result_packet.append(int(self.number_to_append))
        self.number_to_append = ''
    
    def append_packet(self):
        packet_to_append = (PacketParser(self.packet_to_append)).parse()
        self.result_packet.append(packet_to_append)
        self.opening_count = self.closing_count = 0
        self.packet_to_append = ''
    
class PacketComparer:
    def __init__(self, first, second) -> None:
        self.assign_packets(first, second)
        
    def compare(self) -> bool:
        if isinstance(self.first, list) and isinstance(self.second, list):
            return self.compare_lists()
        else:
            return self.compare_numbers()
        
    def compare_lists(self):
        i = 0    
        while True:
            if len(self.first) == i and len(self.second) > i:
                return True
            elif len(self.first) > i and len(self.second) == i:
                return False
            elif len(self.first) == i and len(self.second) == i:
                break
            
            result = (PacketComparer(self.first[i], self.second[i])).compare()
            if result is not None:
                return result
            i += 1
        
    def compare_numbers(self):
        return None if self.first == self.second else self.first < self.second
    
    def assign_packets(self, first, second):        
        if isinstance(first, list) and not isinstance(second, list):
            second = [second]
        elif isinstance(second, list) and not isinstance(first, list):
            first = [first]
        self.first = first
        self.second = second
    
def get_indices_sum(chunks):
    indices_sum = 0
    i = 1
    for chunk in chunks:
        left = (PacketParser(chunk[0].strip())).parse()
        right = (PacketParser(chunk[1].strip())).parse()
        in_right_order = (PacketComparer(left, right)).compare()
        if in_right_order:
            indices_sum += i
        i += 1
        
    return indices_sum

def get_divider_indices_product(chunks):
    divider_packets = {
        0: {
            'value': [[2]],
            'preceding_packets': 0,
        },
        1: {
            'value': [[6]],
            'preceding_packets': 1, # because [[2]] is preceding too
        },
    }
    for chunk in chunks:
        for line in chunk[:2]:
            packet = (PacketParser(line.strip())).parse()
            for k in divider_packets:
                divider_packet = divider_packets[k]['value']
                comparer = PacketComparer(packet, divider_packet)
                if comparer.compare():
                    divider_packets[k]['preceding_packets'] += 1
                    
    return reduce(lambda x, y: x * y, [v['preceding_packets'] + 1 for v in divider_packets.values()])
        
with open('2022/input13.txt') as f:
    chunks = list(divide_chunks(f.readlines(), 3))
    print(get_indices_sum(chunks)) # Part One
    print(get_divider_indices_product(chunks)) # Part Two
