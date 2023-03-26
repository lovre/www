import re
import os

class GraphException(Exception):
  """
  Class representing graph exception.
  """
  
  def __init__(self, message):
    super().__init__("GraphException: " + message)

class NodeException(GraphException):
  """
  Class representing node exception raised when node does not exist.
  """
  
  def __init__(self, i):
    super().__init__("node with index {:d} does not exist".format(i))

class EdgeException(GraphException):
  """
  Class representing edge exception raised when edge does not exist.
  """
  
  def __init__(self, i, j):
    super().__init__("edge between nodes {:d} and {:d} does not exist".format(i, j))

class UnsupportedException(Exception):
  """
  Class representing exception raised when unsupported function is called.
  """
  
  def __init__(self):
    super().__init__("Exception: unsupported function for this class")
    
class Graph:
  """
  Class storing undirected graph without loops represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing the graph and adding nodes or edges.
  """
  
  def __init__(self, name, n = 0):
    self.A = [[] for _ in range(n)]
    self.name = name
    self.L = None
    self.n = n
    self.m = 0
    
  #
  #   -- GRAPH --
  #

  def get_name(self):
    return self.name

  def get_n(self):
    return self.n
  
  def get_m(self):
    return self.m
  
  def get_k(self):
    return 2 * self.m / self.n if self.n > 0 else 0
    
  def is_simple(self):
    for a in self.A:
      if len(set(a)) < len(a):
        return False
        
    return True

  def is_multi(self):
    return not self.is_simple()
  
  def is_labeled(self):
    return self.L is not None
    
  def __str__(self):
    return "{:>12s} | '{:s}'\n{:>12s} | '{:s}'\n{:>12s} | {:,d}\n{:>12s} | {:,d}\n{:>12s} | {:.2f}\n".format('Graph', self.name, 'Type', ('x' if self.is_labeled() else '0') + ('--' if self.is_simple() else '==') + ('y' if self.is_labeled() else '1'), 'Nodes', self.n, 'Edges', self.m, 'Degree', self.get_k())
  
  #
  #   -- NODES --
  #
  
  def get_nodes(self):
    return list(range(self.n))
    
  def is_node(self, i):
    return i >= 0 and i < self.n
    
  def get_neighbours(self, i):
    if not self.is_node(i):
      raise NodeException(i)
      
    return self.A[i]
    
  def get_degree(self, i):
    return len(self.get_neighbours(i))
    
  def get_label(self, i):
    if not self.is_node(i):
      raise NodeException(i)
      
    return None if self.L is None else self.L[i]
    
  def set_label(self, i, label = None):
    if not self.is_node(i):
      raise NodeException(i)
      
    if self.L is None:
      self.L = [None for _ in range(self.n)]
      
    self.L[i] = label

  def add_node(self, label = None):
    self.n += 1
    self.A.append([])
    
    if label is not None:
      if self.L is None:
        self.L = [None for _ in range(self.n - 1)]
      self.L.append(label)

    return self.n - 1
    
  #
  #   -- EDGES --
  #
  
  def get_edges(self):
    return [(i, j) for i in range(self.n) for j in self.get_neighbours(i) if i < j]

  def is_edge(self, i, j):
    if not self.is_node(i):
      raise NodeException(i)
    elif not self.is_node(j):
      raise NodeException(j)
      
    return j in self.get_neighbours(i)

  def add_edge(self, i, j):
    if not self.is_node(i):
      raise NodeException(i)
    elif not self.is_node(j):
      raise NodeException(j)
      
    self.A[i].append(j)
    self.A[j].append(i)
    self.m += 1

  def remove_edge(self, i, j):
    if not self.is_edge(i, j):
      raise EdgeException(i, j)
      
    self.A[i].remove(j)
    self.A[j].remove(i)
    self.m -= 1

  #
  #   -- I/O --
  #
  
  @staticmethod
  def read(name, path = '.'):
    """
    Read graph from the specified file in Pajek format.
    Function returns graph G represented by class Graph.
    """
    
    G = None
    with open(os.path.join(path, name + '.net'), 'r') as file:
      for line in file:
        if re.match(r'^\*vertices', line):
          G = Graph(name, int(re.split('\s+', line)[1]))
        elif re.match(r'^\*(edges|arcs)', line):
          break
        else:
          node = re.split('"', line)
          if len(node) > 1 and len(node[1]):
            G.set_label(int(node[0]) - 1, node[1])
            
      for line in file:
        edge = re.split('\s+', line)
        G.add_edge(int(edge[0]) - 1, int(edge[1]) - 1)
        
    return G
  
  @staticmethod
  def write(G, path = '.'):
    """
    Write graph G to file in Pajek format specified by graph name.
    Function returns graph G represented by class Graph.
    """
    
    with open(os.path.join(path, G.get_name() + '.net'), 'w') as file:
      file.write('*vertices {:d}\n'.format(G.get_n()))
      
      for i in G.get_nodes():
        file.write('{:d}{:s}\n'.format(i + 1, ' "' + G.get_label(i) + '"' if G.is_labeled() and G.get_label(i) is not None else ''))
        
      file.write('*edges {:d}\n'.format(G.get_m()))
      
      for i, j in G.get_edges():
        file.write('{:d} {:d}\n'.format(i + 1, j + 1))
        
    return G

class Path(Graph):
  """
  Class storing undirected path graph represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing (path) graph and adding new nodes to the path.
  """
  
  def __init__(self, name, n = 0):
    super().__init__(name, n)
    
    for i in range(n - 1):
      super().add_edge(i, i + 1)

  def add_node(self, label = None):
    super().add_node(label)
    super().add_edge(self.n - 2, self.n - 1)
    
    return self.n - 1

  def add_edge(self, i, j):
    raise UnsupportedException()
    
  def remove_edge(self, i, j):
    raise UnsupportedException()

class Cycle(Graph):
  """
  Class storing undirected cycle graph represented by its name, adjacency list A and node labels L.
  Class contains standard functions for accessing (cycle) graph and adding new nodes to the cycle.
  """
  
  def __init__(self, name, n = 0):
    super().__init__(name, n)
    
    for i in range(n):
      super().add_edge(i, (i + 1) % n)
    
  def add_node(self, label = None):
    super().add_node(label)
    super().remove_edge(0, self.n - 2)
    super().add_edge(self.n - 2, self.n - 1)
    super().add_edge(0, self.n - 1)
    
    return self.n - 1

  def add_edge(self, i, j):
    raise UnsupportedException()
    
  def remove_edge(self, i, j):
    raise UnsupportedException()
    
# constructs demo graph G represented by class Graph

G = Graph("demo")

G.add_node("foo")
G.add_node("bar")
G.add_node("baz")
G.add_node()

G.add_edge(0, 1)
G.add_edge(1, 2)
G.add_edge(1, 2)

# prints out standard information of demo graph G

print(G)

# constructs and prints out standard information of path graph P

P = Path("path", 10)

print(P)

# constructs and prints out standard information of cycle graph C

C = Cycle("cycle", 10)

print(C)

# prints out standard information of real networks

print(Graph.read('karate_club'))
print(Graph.read('dolphins'))
print(Graph.read('imdb'))
