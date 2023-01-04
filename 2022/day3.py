import string

priorities = {}
for i, letter in enumerate(string.ascii_letters, start=1):
    priorities[letter] = i
        
'''Part One'''
# result = 0;
# with open('2022/input3.txt') as f:
#     for line in f.readlines():
#         line = line.strip()
#         l = int(len(line) / 2)
#         first_comp = line[:l]
#         second_comp = line[l:]
#         for item in first_comp:
#             if item in second_comp:
#                 result += priorities[item]
#                 break
       
       
'''Part Two'''

# Yield successive n-sized
# chunks from l.
def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
result = 0;
with open('2022/input3.txt') as f:
    chunks = list(divide_chunks(f.readlines(), 3))
    for chunk in chunks:
        first = chunk[0].strip()
        second = chunk[1].strip()
        third = chunk[2].strip()
        for item in first:
            if item in second and item in third:
                result += priorities[item]
                break
            
print(result)