import importlib
import inspect
import sys
import time
from pathlib import Path
        
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = 1000 * (time.time() - start_time)
        print('***** %s *****' % func.__name__.title().replace('_', ' '))
        print(f'Result: {result}')
        print(f'Duration: {duration} ms', end="\n\n")
        
    return wrapper
        
class Runner:
    def __init__(self, day, test=False, part=None) -> None:
        self.year = '2023'
        self.day = day
        self.test = test
        self.part = part
    
    def run(self):
        mod = importlib.import_module('{y}.{d}.solution'.format(y = self.year, d = self.day))
        solution = mod.Solution(self.test)
        
        if self.part is None or self.part == '1':
            solution.part_one()
        
        if self.part is None or self.part == '2':
            solution.part_two()
        
class BaseSolution:
    def __init__(self, is_test) -> None:
        self.is_test = is_test
        
    def __getattribute__(self, name):
        if name.startswith('part'):
            self.set_path(name[-1])
            
        return object.__getattribute__(self, name)
    
    @timer
    def part_one(self,):
        return self.part1()
    
    @timer
    def part_two(self,):
        return self.part2()
            
    def set_path(self, part):
        self.input_filename = 'test{0}.txt'.format(part) if self.is_test else 'input.txt'
        self.path = Path(inspect.getfile(self.__class__)).with_name(self.input_filename)
                    
        
if __name__ == "__main__":
    day = sys.argv[1]
    test = 'test' in sys.argv
    
    part = None
    for arg in sys.argv:
        if arg.startswith('--part='):
            part = arg.split('=')[-1]
            break
    
    runner = Runner(day, test, part)
    runner.run()
        
    