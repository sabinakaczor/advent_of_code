import importlib
import inspect
import sys
import time
from pathlib import Path

class Runner:
    def __init__(self, day, test=False) -> None:
        self.year = '2023'
        self.day = day
        self.test = test
    
    def run(self):
        mod = importlib.import_module('{y}.{d}.solution'.format(y = self.year, d = self.day))
        solution = mod.Solution(self.test)
        start_time = time.time()
        solution.run()
        duration = time.time() - start_time
        print("--- %s seconds ---" % duration)
        
class BaseSolution:
    def __init__(self, is_test) -> None:
        self.is_test = is_test
        
    def __getattribute__(self, name):
        if name.startswith('part'):
            self.set_path(name[-1])
            
        return object.__getattribute__(self, name)
            
    def set_path(self, part):
        self.input_filename = 'test{0}.txt'.format(part) if self.is_test else 'input.txt'
        self.path = Path(inspect.getfile(self.__class__)).with_name(self.input_filename)
                    
        
if __name__ == "__main__":
    day = sys.argv[1]
    test = len(sys.argv) > 2 and sys.argv[2] == 'test'
    runner = Runner(day, test)
    runner.run()
        
    