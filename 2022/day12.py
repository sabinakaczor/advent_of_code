import sys, heapq

sys.path.append('.')

from modules.graph import DirectedGraph

class HillClimbingAlgorithm:
    
    def __init__(self, heightmap: list) -> None:
        self.heightmap = heightmap
        
    def goal_reached(self, vertex):
        return vertex.get_vertex_id() == self.best_signal_position
    
    def get_fewest_steps_required(self) -> int:
        self.scan_map()
        return self.get_fewest_steps_required_from_position(self.starting_position)
        
    def get_fewest_steps_required_from_position(self, frm) -> int:
        source = self.graph.get_vertex(frm)
        source.set_distance(0)
        unvisited_queue = [(v.get_distance(), v.get_vertex_id(), v) for v in self.graph]
        heapq.heapify(unvisited_queue)
        while len(unvisited_queue):
            uv = heapq.heappop(unvisited_queue)
            current = uv[2]
            current.set_visited()
            for next in current.get_connections():
                if next.visited:
                    continue
                new_dist = current.get_distance() + current.get_weight(next)
                if new_dist < next.get_distance():
                    next.set_distance(new_dist)
                    next.set_previous(current)
                    
                if self.goal_reached(next):
                    return next.get_distance()
                    
            while len(unvisited_queue):
                heapq.heappop(unvisited_queue)
                
            unvisited_queue = [(v.get_distance(), v.get_vertex_id(), v) for v in self.graph if not v.visited]
            heapq.heapify(unvisited_queue)
            
        return -1
    
    def get_slope(self, first: str, second: str) -> int:
        """positive slope means that second is higher than first"""
        return self.get_ord(second) - self.get_ord(first)
    
    def get_ord(self, square) -> int:
        if square == 'S':
            return ord('a')
        elif square == 'E':
            return ord('z')
        
        return ord(square)
    
    def scan_map(self):
        self.basic_direction_condition = lambda slope: slope <= 1
        self.inverse_direction_condition = lambda slope: slope >= -1
        self.heightmap_width = len(self.heightmap[0])
        self.heightmap_height = len(self.heightmap)
        self.graph = DirectedGraph()
        
        for l, row in enumerate(self.heightmap):
            for k, square in enumerate(row):
                i = l * self.heightmap_width + k
                self.graph.add_vertex(i)
                
        for l, row in enumerate(self.heightmap):
            for k, square in enumerate(row):
                i = l * self.heightmap_width + k
                self.discover_edges(i, square, k, row, l)
                
                if square == 'S':
                    self.starting_position = i
                elif square == 'E':
                    self.best_signal_position = i
                    
    def discover_edges(self, i, square, k, row, l):
        if k < self.heightmap_width - 1:
            right_square = row[k+1]
            slope = self.get_slope(square, right_square)
            if self.basic_direction_condition(slope):
                self.graph.add_edge(i, i+1, 1)
            if self.inverse_direction_condition(slope):
                self.graph.add_edge(i+1, i, 1)
            
        if l < self.heightmap_height - 1:
            down_square = self.heightmap[l+1][k]
            slope = self.get_slope(square, down_square)
            if self.basic_direction_condition(slope):
                self.graph.add_edge(i, i+self.heightmap_width, 1)
            if self.inverse_direction_condition(slope):
                self.graph.add_edge(i+self.heightmap_width, i, 1)
    
    def print_path(self):
        path = ['.'] * self.heightmap_width * self.heightmap_height
        path[self.best_signal_position] = 'E'
        current = self.graph.vert_dictionary[self.best_signal_position]
        previous = current.get_previous()
        while previous is not None:
            k = current.get_vertex_id()
            p = previous.get_vertex_id()
            if p == k+1:
                path[p] = '<'
            elif p == k-1:
                path[p] = '>'
            elif p == k+self.heightmap_width:
                path[p] = '^'
            elif p == k-self.heightmap_width:
                path[p] = 'v'
            current = previous
            previous = current.get_previous()
            
        i = 0
        while i < len(path):
            print(''.join(path[i : i+self.heightmap_width]))
            i += self.heightmap_width
            

class HillClimbingAlgorithmPartTwo(HillClimbingAlgorithm):    
        
    def goal_reached(self, vertex):
        return vertex.get_vertex_id() in self.lowest_positions
    
    def get_fewest_steps_required(self) -> int:
        self.scan_map()
        return self.get_fewest_steps_required_from_position(self.best_signal_position)
    
    def scan_map(self):
        self.basic_direction_condition = lambda slope: slope >= -1
        self.inverse_direction_condition = lambda slope: slope <= 1
        self.heightmap_width = len(self.heightmap[0])
        self.heightmap_height = len(self.heightmap)
        self.graph = DirectedGraph()
        self.lowest_positions = []
        
        for l, row in enumerate(self.heightmap):
            for k, square in enumerate(row):
                i = l * self.heightmap_width + k
                self.graph.add_vertex(i)
                
        for l, row in enumerate(self.heightmap):
            for k, square in enumerate(row):
                i = l * self.heightmap_width + k
                self.discover_edges(i, square, k, row, l)
                
                if square == 'S':
                    self.starting_position = i
                    self.lowest_positions.append(i)
                elif square == 'E':
                    self.best_signal_position = i
                elif square == 'a':
                    self.lowest_positions.append(i)

with open('2022/input12.txt') as f:
    heightmap = [list(line.strip()) for line in f.readlines()]
    algorithm = HillClimbingAlgorithmPartTwo(heightmap)
    steps = algorithm.get_fewest_steps_required()
    print(steps)