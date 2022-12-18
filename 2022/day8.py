from functools import reduce

def is_highest(height, other_heights):    
    for h in other_heights:
        if h >= height:
            return False
    return True

def count_visible_trees(rows):    
    visible_count = 0
    for r, row in enumerate(rows):
        for c, height in enumerate(row):
            '''first check if tree is on the edge'''
            if r == 0 or c == 0 or r == len(rows) - 1 or c == len(row) - 1:
                visible_count += 1
                '''if it isn\'t, compare its height to other trees'''
            else:
                trees = {
                    'on_the_left': row[:c],
                    'on_the_right': row[c+1:],
                    'on_the_top':  [x[c] for x in rows[:r]],
                    'on_the_bottom': [x[c] for x in rows[r+1:]],
                }
                
                for k in trees:
                    if is_highest(height, trees[k]):
                        visible_count += 1
                        break
    return visible_count

def find_viewing_distance(height, other_heights, rev = False):
    distance = 0;
    if rev:
        other_heights.reverse()
    for h in other_heights:
        distance += 1
        if h >= height:
            break
        
    return distance

def find_highest_scenic_score(rows):    
    highest_score = 0
    for r, row in enumerate(rows):
        row = [int(x) for x in row]
        for c, height in enumerate(row):
            '''first check if tree is on the edge'''
            if not (r == 0 or c == 0 or r == len(rows) - 1 or c == len(row) - 1):                
                trees = {
                    'on_the_left': (row[:c], True),
                    'on_the_right': (row[c+1:], False),
                    'on_the_top':  ([int(x[c]) for x in rows[:r]], True),
                    'on_the_bottom': ([int(x[c]) for x in rows[r+1:]], False),
                }
                
                distances = [find_viewing_distance(height, trees[k][0], trees[k][1]) for k in trees]
                
                score = reduce(lambda x, y: x * y, distances)
                if score > highest_score:
                    highest_score = score
                
    return highest_score


with open('input8.txt') as f:
    rows = [line.strip() for line in f]

'''Part One'''
# print(count_visible_trees(rows))

'''Part Two'''
print(find_highest_scenic_score(rows))
                