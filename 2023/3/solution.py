from run import BaseSolution

class Solution(BaseSolution):
    symbol = None
        
    def part1(self):
        total = 0
        with self.path.open() as f:
            chars_map = [list(line.rstrip()) for line in f]
            self.build_maps(chars_map)
            for number, positions in self.numbers_map.items():
                for pos_data in positions:
                    if self.number_has_symbol(pos_data):
                        total += number
                    
        return total

    def number_has_symbol(self, pos_data):
        start, end = pos_data
        
        # check the rows over and below the number row
        for x in [start[0], end[0]]:
            for y in range(start[1], end[1] + 1):
                if y in self.symbols_map.get(x, []):
                    return True

        # check the cells on sides of the number
        number_row_symbols = self.symbols_map.get(start[0] + 1, [])
        if start[1] in number_row_symbols or end[1] in number_row_symbols:
            return True
        
        return False
        
    def part2(self):
        self.symbol = '*'
        total = 0
        with self.path.open() as f:
            chars_map = [list(line.rstrip()) for line in f]
            self.build_maps(chars_map)
            for row, cols in self.symbols_map.items():
                for col in cols:
                    total += self.find_gear_ratio(row, col)
                    
        return total

    def find_gear_ratio(self, row, col):
        numbers = []
        for number, positions in self.numbers_map.items():
            for pos_data in positions:
                start, end = pos_data
                if row < start[0] or row > end[0] or col < start[1] or col > end[1]:
                    continue
                numbers.append(number)
                if len(numbers) > 2:
                    return 0
                
        if len(numbers) < 2:
            return 0
        
        return numbers[0] * numbers[1]
                            
    def build_maps(self, chars_map):
        self.symbols_map = {}
        self.numbers_map = {}
        for row, line in enumerate(chars_map, start=1):
            self.symbols_map[row] = []
            self.parse_line(line, row)
                
    def parse_line(self, line, row):
        current_number = ''
        for col, ch in enumerate(line, start=1):
            if ch.isnumeric():
                if not current_number:
                    start_pos = [row-1, col-1]
                current_number += ch
            else:
                if ch != '.' and (self.symbol is None or ch == self.symbol):
                    self.symbols_map[row].append(col)
                if current_number:
                    self.add_number_data(current_number, row, col, start_pos)
                    current_number = ''
        if current_number:
            self.add_number_data(current_number, row, col, start_pos)
    
    def add_number_data(self, current_number, row, col, start_pos):
        end_pos = [row+1, col]
        pos_data = (
            start_pos,
            end_pos
        )
        number_int = int(current_number)
        if number_int in self.numbers_map:
            self.numbers_map[number_int].append(pos_data)
        else:
            self.numbers_map[number_int] = [pos_data]