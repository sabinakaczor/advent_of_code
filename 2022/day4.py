'''Part One'''

# result = 0;
# with open('2022/input4.txt') as f:
#     for line in f.readlines():
#         line = line.strip()
#         ranges = line.split(',')
#         [start1, end1] = [int(x) for x in ranges[0].split('-')]
#         [start2, end2] = [int(x) for x in ranges[1].split('-')]
#         range1 = range(start1, end1 + 1)
#         range2 = range(start2, end2 + 1)
#         if (start1 in range2 and end1 in range2) or (start2 in range1 and end2 in range1):
#             result += 1
            
'''Part Two'''

result = 0;
with open('2022/input4.txt') as f:
    for line in f.readlines():
        line = line.strip()
        ranges = line.split(',')
        [start1, end1] = [int(x) for x in ranges[0].split('-')]
        [start2, end2] = [int(x) for x in ranges[1].split('-')]
        len1 = len(range(start1, end1 + 1))
        len2 = len(range(start2, end2 + 1))
        total_range = range(min(start1, start2), max(end1, end2) + 1)
        if len(total_range) < len1 + len2:
            result += 1
            
print(result)
        