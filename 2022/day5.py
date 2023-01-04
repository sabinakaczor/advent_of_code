import re

crates_info = []
pattern = re.compile(r'^move (?P<count>\d+) from (?P<from>\d) to (?P<to>\d)$')

def divide_chunks(line):
    # looping till length l
    for i in range(0, len(line), 4):
        yield line[i:i + 3]

def parse_crates_line(line):
    chunks = list(divide_chunks(line))
    crates_info.insert(0, chunks)
    
def process_crates_info():
    global crates
    indices = [int(i.strip()) for i in crates_info.pop(0)]
    crates = [[] for i in indices]
    for row in crates_info:
        for i, crate in enumerate(row):
            crate = crate.strip()
            if crate:
                crates[i].append(crate[1:-1])
    crates = dict(zip(indices, crates))
 
'''Step One'''   
# def follow_procedure(step):
#     global crates
#     pattern = re.compile(r'^move (?P<count>\d+) from (?P<from>\d) to (?P<to>\d)$')
#     m = re.match(pattern, step)
#     if m:
#         [count, fromS, toS] = [int(x) for x in m.group('count', 'from', 'to')]
#         for i in range(count):
#             crate = crates[fromS].pop()
#             crates[toS].append(crate)
            
'''Step Two'''   
def follow_procedure(step):
    global crates
    m = re.match(pattern, step)
    if m:
        [count, fromS, toS] = [int(x) for x in m.group('count', 'from', 'to')]
        crates[toS] += crates[fromS][-count:]
        crates[fromS] = crates[fromS][:-count]
        

with open('2022/input5.txt') as f:
    steps_reached = False
    for line in f:
        if line == '\n':
            steps_reached = True
            process_crates_info()
        else:
            if steps_reached:
                '''Follow the next step of the procedure.'''
                follow_procedure(line)
            else:
                '''Parse the next line of crates.'''
                parse_crates_line(line)
                
top_crates = [crates[x].pop() for x in crates]
print(''.join(top_crates))
            