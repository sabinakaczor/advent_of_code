class Rope:
    
    DIRECTION_RIGHT = 'R'
    DIRECTION_LEFT = 'L'
    DIRECTION_UP = 'U'
    DIRECTION_DOWN = 'D'
    
    visited_by_tail = set()
    knot_positions = []
    
    def __init__(self, knots_count) -> None:
        self.knots_count = knots_count
        self.prepare()
        
    def prepare(self):
        for i in range(self.knots_count):
            self.knot_positions.append([0,0])
        self.visited_by_tail.add(tuple(self.knot_positions[i]))
        
    def move_head(self, direction, steps):
        step = 1 if direction == self.DIRECTION_RIGHT or direction == self.DIRECTION_UP else -1
        index = 0 if direction == self.DIRECTION_RIGHT or direction == self.DIRECTION_LEFT else 1
           
        for i in range(steps):     
            self.knot_positions[0][index] += step
            self.update_knot_positions()
    
    def update_knot_positions(self):
        for i in range(1, len(self.knot_positions)):
            self.update_knot_position(i)
                
        self.visited_by_tail.add(tuple(self.knot_positions[i]))
        
    def update_knot_position(self, index):
        preceding_knot = self.knot_positions[index-1]
        processed_knot = self.knot_positions[index]
        
        dim = self.get_dim_with_two_steps_directly(preceding_knot, processed_knot)
        if dim != None:
            self.move_knot_one_step_towards_preceding_in_given_dimension(dim, preceding_knot, processed_knot)
        elif not self.check_if_touching(preceding_knot, processed_knot):
            for i in (0,1):
                self.move_knot_one_step_towards_preceding_in_given_dimension(i, preceding_knot, processed_knot)
                
    def move_knot_one_step_towards_preceding_in_given_dimension(self, dim, preceding_knot, processed_knot):        
        step = 1 if preceding_knot[dim] - processed_knot[dim] > 0 else -1
        processed_knot[dim] += step
                    
    def get_dim_with_two_steps_directly(self, first, second):
        for i in (0,1):
            j = 1 - i
            if first[i] == second[i] and abs(first[j] - second[j]) == 2:
                return j
                    
    def check_if_touching(self, first, second):
        for i in (0,1):
            if abs(first[i] - second[i]) >= 2:
                return False
        return True
      
    def get_number_positions_of_visited_by_tail(self):
          return len(self.visited_by_tail)
      
with open('input9.txt') as f:
    r = Rope(10)
    for line in f:
        parts = line.strip().split(' ')
        direction = parts[0]
        steps = int(parts[1])
        r.move_head(direction, steps)
    print(r.get_number_positions_of_visited_by_tail())