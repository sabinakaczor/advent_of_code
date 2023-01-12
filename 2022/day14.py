from copy import copy

PART = 2

class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        
    def to_tuple(self):
        return (self.x, self.y)
    
class Scan:
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int) -> None:
        self.dict = {}
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.starting_point = Point(500, 0)
    
    def prepare_dict(self):
        for x in range(self.min_x, self.max_x + 1):
            for y in range(self.min_y, self.max_y + 1):
                self.dict[(x,y)] = '.'
        self.dict[self.starting_point.to_tuple()] = '+'
        
    def fill_dict_with_paths(self, paths: list): 
        if not self.dict:
            self.prepare_dict()       
        for path in paths:
            prev_p  = None
            for point in path:
                self.dict[point] = '#'
                if prev_p is not None:
                    self.discover_line(prev_p, Point(*point))
                prev_p = Point(*point)
                
    def discover_line(self, previous: Point, current: Point):
        range_x = [current.x] if previous.x == current.x else range(min(previous.x, current.x), max(previous.x, current.x) + 1)
        range_y = [current.y] if previous.y == current.y else range(min(previous.y, current.y), max(previous.y, current.y) + 1)
        for x in range_x:
            for y in range_y:
                self.dict[(x,y)] = '#'                
                
    def print_scan(self):
        for y in range(self.min_y, self.max_y + 1):
            for x in range(self.min_x, self.max_x + 1):
                print(self.dict[(x,y)], end='') 
            print('')
    
    def get_counter(self):
        return self.counter
    
class ScanWithAbyss(Scan):            
    def simulate_sand(self):        
        self.counter = 0
        break_outermost = False
        
        while True:
            # iteration for the movement of one unit of sand
            current_pos = copy(self.starting_point)
            try_counter = 0
            abyss_reached = False
            
            while True:
                # iteration for one single move
                try_counter += 1
                investigated_positions = (
                    (current_pos.x, current_pos.y + 1),
                    (current_pos.x - 1, current_pos.y + 1),
                    (current_pos.x + 1, current_pos.y + 1),
                )
                
                for t in investigated_positions:
                    investigated_pos = Point(*t)
                    
                    if t not in self.dict:                    
                        abyss_reached = True
                        self.dict[current_pos.to_tuple()] = '.'
                        break
                    elif self.dict[t] == '.':
                        if try_counter > 1:
                            self.dict[current_pos.to_tuple()] = '.'
                        self.dict[t] = 'o'
                        current_pos = investigated_pos
                        break
                else:   
                    # abyss not reached, but no place to rest  
                    self.counter += 1
                    break
                
                if abyss_reached:
                    break_outermost = True
                    break
            
            if break_outermost:
                break
    
class ScanWithFloor(Scan):       
    def prepare_dict(self):
        self.max_y += 2
        super().prepare_dict()
        for x in range(self.min_x, self.max_x + 1):
            self.dict[(x,self.max_y)] = '#'     
            
    def extend_dict(self, new_x):
        r = []
        if new_x < self.min_x:
            r = range(new_x, self.min_x)
            self.min_x = new_x
        elif new_x > self.max_x:
            r = range(self.max_x + 1, new_x + 1)
            self.max_x = new_x
        for x in r:
            for y in range(self.min_y, self.max_y):
                self.dict[(x, y)] = '.'
            self.dict[(x, self.max_y)] = '#'
         
    def simulate_sand(self):        
        self.counter = 0
        break_outermost = False
        
        while True:
            # iteration for the movement of one unit of sand
            current_pos = copy(self.starting_point)
            try_counter = 0
            
            while True:
                # iteration for one single move
                current_tuple = current_pos.to_tuple()
                self.dict[current_tuple] = 'o'
                try_counter += 1
                
                investigated_positions = (
                    (current_pos.x, current_pos.y + 1),
                    (current_pos.x - 1, current_pos.y + 1),
                    (current_pos.x + 1, current_pos.y + 1),
                )
                
                for t in investigated_positions:
                    investigated_pos = Point(*t)
                    
                    if t not in self.dict and t[1] <= self.max_y:
                        self.extend_dict(t[0])
                        
                    if t in self.dict and self.dict[t] == '.':
                        self.dict[current_tuple] = '+' if try_counter == 1 else '.'
                        self.dict[t] = 'o'
                        current_pos = investigated_pos
                        break
                else:   
                    # no place to rest 
                    self.counter += 1
                    if current_tuple == self.starting_point.to_tuple():
                        break_outermost = True
                    break
            
            if break_outermost:
                break
        
sketch = {}

def get_scan_object(*args) -> Scan: 
    if PART == 1:   
        return ScanWithAbyss(*args)
    elif PART == 2:
        return ScanWithFloor(*args)
    
def get_scan(lines):
    paths = []
    min_y = 0
    min_x = max_x = max_y = None
    for line in lines:
        points = line.strip().split(' -> ')
        points = [tuple(map(int, point.split(','))) for point in points]
        paths.append(points)
        
        for point in points:
            x = point[0]
            y = point[1]
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y
                
    scan = get_scan_object(min_x, max_x, min_y, max_y)
    scan.fill_dict_with_paths(paths)
    
    return scan
    
with open('2022/input14.txt') as f:
    scan = get_scan(f)
    scan.simulate_sand()
    print(scan.get_counter())
    # scan.print_scan()
    