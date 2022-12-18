import pprint
from functools import reduce

TOTAL_SPACE = 70000000
NEEDED_SPACE = 30000000

filesystem_tree = {
    '/': {
        'dirs': {},
        'files': {}
    }
}
current_path_parts = []
total_size = 0

def parse_command(line):
    global current_path_parts
    parts = line.split(' ')[1:]
    command = parts.pop(0)
    if command == 'cd':
        target = parts[0]
        if target == '..':
            current_path_parts.pop()
        elif target[0] == '/':
            current_path_parts = ['/']
        elif target != '.':
            current_path_parts.append(target)

def parse_output(line):
    if line[:4] == 'dir ':
        dirname = line[4:]
        attach_dir_to_current_path(dirname)
    else:
        [size, name] = line.split(' ')
        attach_file_to_current_path(name, size)
        
def attach_dir_to_current_path(dirname):
    ref = filesystem_tree[current_path_parts[0]]['dirs']
    for part in current_path_parts[1:]:
        if part not in ref:
            ref[part] = {
                'dirs': {},
                'files': {}
            }
        ref = ref[part]['dirs']
    ref[dirname] = {
        'dirs': {},
        'files': {}
    }
    
def attach_file_to_current_path(name, size):
    ref = filesystem_tree[current_path_parts[0]]
    for part in current_path_parts[1:]:
        ref = ref['dirs'][part]
    ref['files'][name] = int(size)
    
def count_dir_size(dir_info):
    global total_size
    size = reduce(lambda x, y: x + y, dir_info['files'].values(), 0)
    for dirname in dir_info['dirs']:
        size += count_dir_size(dir_info['dirs'][dirname])
    dir_info['size'] = size
    
    '''Step One - counting the sum of the total sizes of the directories with a total size of at most 100000'''
    # if size <= 100000:
    #     total_size += size
        
    return size

def check_dir_size(dir_info):
    global size_of_dir_to_remove
    if dir_info['size'] >= missing_space and dir_info['size'] < size_of_dir_to_remove:
        size_of_dir_to_remove = dir_info['size']
    for dirname in dir_info['dirs']:
        check_dir_size(dir_info['dirs'][dirname])
        
with open('input7.txt') as f:
    for line in f:
        line = line.rstrip()
        command_mode = line[:2] == '$ '
        if command_mode:
            '''Parse command'''
            parse_command(line)
        else:
            '''Parse output'''
            parse_output(line)
            
count_dir_size(filesystem_tree['/'])
used_space = filesystem_tree['/']['size']
free_space = TOTAL_SPACE - used_space
missing_space = NEEDED_SPACE - free_space
size_of_dir_to_remove = used_space
check_dir_size(filesystem_tree['/'])

print(missing_space, size_of_dir_to_remove)

'''Step One - the sum of the total sizes of the directories with a total size of at most 100000'''
# print(total_size)