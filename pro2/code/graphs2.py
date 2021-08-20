from random import *
from time import *
import re
import os

def simple(A):
  """
  Check whether graph represented by adjacency list A is a simple graph.
  Function returns True if the graph is simple and False otherwise.
  """
  for a in A:
    if len(set(a)) < len(a):
      return False
  return True

def gnp(n, p):
  """
  Generate Erdos-Renyi random graph with n nodes and edge probability p.
  Function returns triple consisting of graph name `G(n,p)`, adjacency list A and node labels set to None.
  """
  A = [[] for _ in range(n)]
  for i in range(n):
    for j in range(i + 1, n):
      if random() < p:
        A[i].append(j)
        A[j].append(i)
  return ('G(n,p)', A, None)

def gnm(n, m):
  """
  Generate Erdos-Renyi random graph with n nodes and m edges.
  Function returns triple consisting of graph name `G(n,m)`, adjacency list A and node labels set to None.
  """
  A = [[] for _ in range(n)]
  for _ in range(m):
    i = randint(0, n - 1)
    j = randint(0, n - 1)
    A[i].append(j)
    A[j].append(i)
  return ('G(n,m)', A, None)

def component(A, N, i):
  """
  Find connected component of node i in a graph represented by adjacency list A considering nodes in list N.
  Function returns a list of node indices C in connected component of node i and removes them from list N.
  """
  C = []
  S = []
  N.remove(i)
  S.append(i)
  while S:
    i = S.pop(0)
    C.append(i)
    for j in A[i]:
      if j in N:
        N.remove(j)
        S.insert(0, j)
  return C

def components(A):
  """
  Find connected components of a graph represented by adjacency list A.
  Function returns a list of lists C of node indices in connected components computed by `component(A, N, i)`.
  """
  C = []
  N = set(range(len(A)))
  while N:
    C.append(component(A, N, next(iter(N))))
  return C

def read(name, path = '.'):
  """
  Read graph from specified file in Pajek format.
  Function returns graph G represented by adjacency list A.
  """
  n = 0
  A = []
  L = None
  
  with open(os.path.join(path, name + '.net'), 'r') as file:
    for line in file:
      if re.match(r'^\*vertices', line): # line.startswith('*vertices')
        n = int(re.split('\s+', line)[1]) # int(line.split()[1])
        A = [[] for _ in range(n)]
      elif re.match(r'^\*(edges|arcs)', line): # line.startswith('*edges') or line.startswith('*arcs')
        break
      else:
        node = re.split('\s+', line) # node = line.split()
        if len(node) > 1 and len(node[1]):
          if not L:
            L = [None for _ in range(n)]
          L[int(node[0]) - 1] = node[1][1:-1]

    for line in file:
      edge = re.split('\s+', line) # line.split()
      (i, j) = [int(x) - 1 for x in edge[:2]]
      A[i].append(j)
      A[j].append(i)

  return (name, A, L)

def write(G, path = '.'):
  """
  Write graph G to default file in Pajek format.
  Function returns graph G represented by adjacency list A.
  """
  (name, A, L) = G

  with open(os.path.join(path, name + '.net'), 'w') as file:
    file.write('*vertices {:d}\n'.format(len(A)))
    for i in range(len(A)):
      file.write('{:d}{:s}\n'.format(i + 1, ' "' + L[i] + '"' if L is not None else ''))

    file.write('*edges {:d}\n'.format(sum([len(a) for a in A]) // 2))
    for i, a in enumerate(A):
      for _ in range(a.count(i) // 2):
        file.write('{0:d} {0:d}\n'.format(i + 1))
      for j in a:
        if i < j:
          file.write('{:d} {:d}\n'.format(i + 1, j + 1))

  return G

def info(G):
  """
  Print out standard information of graph G represented by adjacency list A.
  Method prints out graph name and type, number of (isolated) nodes and (self) edges, average node degree, size and number of connected components, average node clustering coefficient and method running time.
  """
  start = time()
  (name, A, L) = G
  
  n = len(A)
  k = [len(a) for a in A]
  m = int(sum(k) / 2)
  C = components(A)

  print("{:>12s} | '{:s}'".format('Graph', name))
  print("{:>12s} | '{:s}'".format('Type', ('x' if L is not None else '0') + ('--' if simple(A) else '==') + ('y' if L is not None else '1')))
  print("{:>12s} | {:,d}".format('Nodes', n))
  print("{:>12s} | {:,d}".format('Edges', m))
  print("{:>12s} | {:.2f}".format('Degree', 2 * m / n))
  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max([len(c) for c in C]) / n, len(C)))
  print("{:>12s} | {:.2f} sec\n".format('Time', time() - start))

# demo graph G represented by adjacency list A and node labels L

A = [[1], [0, 2, 2], [1, 1], []]
L = ['foo', 'bar', 'baz', None]
G = ('demo', A, L)

# prints out standard information of demo graph G

info(G)

# prints out standard information of different random graphs

info(gnm(100000, 250000))

G = gnp(1000, 0.01)
info(G)

# runs simple assertion test for graph reading and writing

assert(write(G) == read(G[0]))

# prints out standard information of different real networks

info(read('karate_club'))
info(read('dolphins'))
info(read('football'))
info(read('highways'))
info(read('facebook'))
info(read('java'))
