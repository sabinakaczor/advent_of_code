def is_unique(s):
    if len(s) == 1:
        return True
    
    for i, char in enumerate(s[1:], start=1):
        if char in s[:i]:
            return False
        
    return True

'''Part One'''
item_length = 4

'''Part Two'''
item_length = 14

with open('input6.txt') as f:
    stream = f.read()
    processed_stream = stream[:item_length-1]
    for s in stream[item_length-1:]:
        processed_stream += s
        if is_unique(processed_stream[-item_length:]):
            break
        
print(len(processed_stream))
            