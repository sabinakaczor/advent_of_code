from run import BaseSolution

class Solution(BaseSolution):

    def part1(self):
        result = 0
        with self.path.open() as f:
            for line in f:
                sequences = self.generate_sequences(self.parse_sequence(line))
                sequences[-1].append(0)
                for i in range(len(sequences)-2, -1, -1):
                    sequences[i].append(sequences[i][-1] + sequences[i+1][-1])
                result += sequences[0][-1]

        return result

    def part2(self):
        result = 0
        with self.path.open() as f:
            for line in f:
                sequences = self.generate_sequences(self.parse_sequence(line))
                sequences[-1].insert(0, 0)
                for i in range(len(sequences)-2, -1, -1):
                    sequences[i].insert(0, sequences[i][0] - sequences[i+1][0])
                result += sequences[0][0]

        return result

    def parse_sequence(self, line):
        return [int(x) for x in line.strip().split(' ')]

    def generate_sequences(self, starting_sequence):
        sequences = [starting_sequence]
        while not self.has_only_zeros(sequences[-1]):
            last_seq = sequences[-1]
            sequences.append([last_seq[i] - last_seq[i-1] for i in range(1, len(last_seq))])

        return sequences

    def has_only_zeros(self, sequence):
        for x in sequence:
            if x:
                return False

        return True
