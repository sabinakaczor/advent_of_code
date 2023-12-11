from run import BaseSolution

class Solution(BaseSolution):

    def parse_input(self):
        galaxies = []
        with self.path.open() as f:
            row = 0
            for line in f:
                row_has_galaxies = False
                col = 0
                for sign in line:
                    if sign == '#':
                        row_has_galaxies = True
                        galaxies.append([row, col])
                    col += 1
                row += 1 if row_has_galaxies else self.expansion_size

            return self.expand_columns(galaxies, col + 1)

    def expand_columns(self, galaxies, columns):
        empty_cols = []
        for i in range(columns):
            galaxies_in_col = [g for g in galaxies if g[1] == i]
            if len(galaxies_in_col) == 0:
                empty_cols.append(i)

        for g in galaxies:
            empty_cols_before = [c for c in empty_cols if c < g[1]]
            g[1] += len(empty_cols_before) * (self.expansion_size - 1)

        return galaxies

    def get_lengths_sum(self):
        galaxies = self.parse_input()
        lengths = []
        for i, galaxy1 in enumerate(galaxies):
            galaxies_to_comp = galaxies[i+1:]
            for galaxy2 in galaxies_to_comp:
                length = abs(galaxy2[0] - galaxy1[0]) + abs(galaxy2[1] - galaxy1[1])
                lengths.append(length)

        return sum(lengths)

    def part1(self):
        self.expansion_size = 2
        return self.get_lengths_sum()

    def part2(self):
        self.expansion_size = 1000000
        return self.get_lengths_sum()
