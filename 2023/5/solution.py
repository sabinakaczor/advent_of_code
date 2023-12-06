from run import BaseSolution

class Solution(BaseSolution):
        
    def part1(self):
        self.map = {}
        with self.path.open() as f:
            content = f.readlines()
            seeds = content[0].split(':')[-1].strip().split(' ')
            self.map = {seed: int(seed) for seed in seeds}            
            
            self.build_map(content)
                  
            return min(self.map.values())
        
    def build_map(self, content):
        expect_header = True
        rows_to_parse = []
        for line in content[2:] + ['']:
            if not line.strip():
                self.parse_map_row(rows_to_parse)
                expect_header = True
                rows_to_parse = []
            elif expect_header:
                expect_header = False
            else:
                rows_to_parse.append(line.strip().split(' '))
                    
    def parse_map_row(self, rows_to_parse):
        for map_source, map_dest in self.map.items():
            for row in rows_to_parse:
                dest_range_start, source_range_start, range_length = [int(value) for value in row]
                if map_dest >= source_range_start and map_dest < source_range_start + range_length:
                    self.map[map_source] = dest_range_start + map_dest - source_range_start
                    break
                