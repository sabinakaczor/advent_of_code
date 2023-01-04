import sys

class G: pass

class Vertex:
    def __init__(self, node) -> None:
        self.id = node
        self.adjacent = {}
        self.distance = 999999
        self.visited = False
        self.previous = None
        
    def add_neighbor(self, neighbor, weight = 0):
        self.adjacent[neighbor] = weight
        
    def get_connections(self):
        return self.adjacent.keys()
    
    def get_vertex_id(self):
        return self.id
    
    def set_vertex_id(self, id):
        self.id = id
        
    def set_visited(self):
        self.visited = True
        
    def get_distance(self):
        return self.distance
        
    def set_distance(self, distance):
        self.distance = distance
        
    def get_previous(self):
        return self.previous
        
    def set_previous(self, previous):
        self.previous = previous
        
    def get_weight(self, neighbor):
        return self.adjacent[neighbor]
        
    def __str__(self) -> str:
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])
    

class Graph(G):
    def __init__(self) -> None:
        self.vert_dictionary = {}
        self.num_vertices = 0
        
    def __iter__(self):
        return iter(self.vert_dictionary.values())
            
    def add_vertex(self, node):
        self.num_vertices += 1
        new_vertex = Vertex(node)
        self.vert_dictionary[node] = new_vertex
        return new_vertex
            
    def get_vertex(self, n):
        if n in self.vert_dictionary:
            return self.vert_dictionary[n]
        return None
            
    def get_vertices(self):
        return self.vert_dictionary.keys()
            
    def get_edges(self):
        edges = []
        for v in self:
            for u in v.get_connections():
                vid = v.get_vertex_id()
                uid = u.get_vertex_id()
                edges.append((vid, uid, v.get_weight(u)))
        return edges
    
class UndirectedGraph(Graph):
    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dictionary:
            self.add_vertex(frm)
        if to not in self.vert_dictionary:
            self.add_vertex(to)
        self.vert_dictionary[frm].add_neighbor(self.vert_dictionary[to], cost)
        self.vert_dictionary[to].add_neighbor(self.vert_dictionary[frm], cost)

class DirectedGraph(Graph):
    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dictionary:
            self.add_vertex(frm)
        if to not in self.vert_dictionary:
            self.add_vertex(to)
        self.vert_dictionary[frm].add_neighbor(self.vert_dictionary[to], cost)
    
if __name__ == '__main__':
    g = DirectedGraph()
    g.add_vertex('a')
    g.add_vertex('b')
    g.add_vertex('c')
    g.add_vertex('d')
    g.add_vertex('e')
    
    # g.add_edge('a', 'e', 10)
    # g.add_edge('a', 'c', 20)
    # g.add_edge('c', 'b', 30)
    # g.add_edge('b', 'e', 40)
    # g.add_edge('e', 'd', 50)
    # g.add_edge('f', 'e', 60)
    
    g.add_edge('a', 'b', 4)
    g.add_edge('a', 'c', 1)
    g.add_edge('b', 'e', 4)
    g.add_edge('c', 'b', 2)
    g.add_edge('c', 'd', 4)
    g.add_edge('d', 'e', 4)
    
    print('Graph data:')
    print(g.get_edges())