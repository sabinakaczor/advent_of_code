from functools import reduce

class RegisterX:
    ROWS_ON_SCREEN = 6
    PIXELS_PER_ROW = 40
    
    def __init__(self, start_value) -> None:
        self.sprite_position = start_value
        self.current_cycle = 1
        self.log = {}
        self.screen = [[] for i in range(self.ROWS_ON_SCREEN)]
        
    def addx(self, value):
        for i in range(2):
            self.add_log()
            self.draw()
            self.current_cycle += 1
        self.sprite_position += value
        
    def noop(self):
        self.add_log()
        self.draw()
        self.current_cycle += 1
        
    def draw(self):
        row = (self.current_cycle - 1) // self.PIXELS_PER_ROW
        position = (self.current_cycle - 1) % self.PIXELS_PER_ROW
        symbol = '#' if position in range(self.sprite_position - 1, self.sprite_position + 2) else '.'
        self.screen[row].append(symbol)
        
    def add_log(self):
        self.log[self.current_cycle] = self.sprite_position
        
    def get_signal_strength(self, cycle):
        return self.log[cycle] * cycle
    
    def render_screen(self):
        for row in self.screen:
            for pixel in row:
                print(pixel, end='')
            print('\n', end='')
   
def part_one(register):    
    cycles = range(20, 221, 40)
    strengths = [register.get_signal_strength(cycle) for cycle in cycles]
    total_signal_strength = reduce(lambda x, y: x + y, strengths)
    print(total_signal_strength)
    
with open('2022/input10.txt') as f:
    register = RegisterX(1)
    for line in f:
        command = line.strip().split(' ')
        if command[0] == 'noop':
            register.noop()
        elif command[0] == 'addx':
            register.addx(int(command[1]))
        
    register.render_screen()
             
             
        