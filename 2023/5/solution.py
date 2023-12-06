from run import BaseSolution

class Solution(BaseSolution):
    with_ranges = False

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
                parsing_func = self.get_parsing_function()
                parsing_func(rows_to_parse)
                expect_header = True
                rows_to_parse = []
            elif expect_header:
                expect_header = False
            else:
                rows_to_parse.append(line.strip().split(' '))

    def get_parsing_function(self):
        return self.parse_rows_with_ranges if self.with_ranges else self.parse_map_row

    def parse_map_row(self, rows_to_parse):
        for map_source, map_dest in self.map.items():
            for row in rows_to_parse:
                dest_range_start, source_range_start, range_length = [int(value) for value in row]
                if map_dest >= source_range_start and map_dest < source_range_start + range_length:
                    self.map[map_source] = dest_range_start + map_dest - source_range_start
                    break

    def part2(self):
        self.with_ranges = True
        self.ranges = []
        with self.path.open() as f:
            content = f.readlines()
            seeds_info = content[0].split(':')[-1].strip().split(' ')
            for pair_no in range(0, len(seeds_info), 2):
                self.ranges.append((int(seeds_info[pair_no]), int(seeds_info[pair_no]) + int(seeds_info[pair_no + 1]) - 1))

            self.build_map(content)

            return min(r[0] for r in self.ranges)

    def parse_rows_with_ranges(self, rows_to_parse):
        unmapped_ranges = self.ranges
        mapped_ranges = []

        for row in rows_to_parse:
            row = [int(x) for x in row]
            map_object = {
                'from': row[1],
                'to': row[1] + row[2] - 1,
                'maps_to': row[0]
            }

            new_mapped, new_unmapped = self.map_ranges(map_object, unmapped_ranges)
            mapped_ranges += new_mapped
            unmapped_ranges = new_unmapped

        self.ranges = mapped_ranges + unmapped_ranges


    def map_ranges(self, map_object, ranges):
        mapped_ranges = []
        unmapped_ranges = []

        for range_item in ranges:
            lower, upper = range_item

            # don't do anything if we can't map at all
            if lower > map_object['to'] or upper < map_object['from']:
                unmapped_ranges.append(range_item)
                continue

            # find and create lower unmapped range
            if lower < map_object['from']:
                unmapped_ranges.append((lower, map_object['from'] - 1))
                lower = map_object['from']

            # find and create upper unmapped range
            if upper > map_object['to']:
                unmapped_ranges.append((map_object['to'] + 1, upper))
                upper = map_object['to']

            # map the actual range
            mapped_ranges.append((
                map_object['maps_to'] + lower - map_object['from'],
                map_object['maps_to'] + upper - map_object['from'],
            ))

        return mapped_ranges, unmapped_ranges
