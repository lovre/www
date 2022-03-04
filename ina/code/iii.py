import time
import random
import networkx as nx
from collections import deque

def isolated(G, i):
  for j in G[i]:
    if j != i:
      return False
  return True
  
def component(G, N, i):
  C = []
  S = []
  N.remove(i)
  S.append(i)
  while S:
    i = S.pop()
    C.append(i)
    for j in G[i]:
      if j in N:
        N.remove(j)
        S.append(j)
  return C

def components(G):
  C = []
  N = set(G.nodes())
  while N:
    C.append(component(G, N, next(iter(N))))
  return C
  
def distance(G, i):
  D = [-1] * len(G) # D = {}
  Q = deque()
  D[i] = 0
  Q.append(i)
  while Q:
    i = Q.popleft()
    for j in G[i]:
      if D[j] == -1: # if j not in D:
        D[j] = D[i] + 1
        Q.append(j)
  return [d for d in D if d > 0]
  
def distances(G, n = 100):
  D = [] # D = {}
  for i in G.nodes() if len(G) <= n else random.sample(G.nodes(), n):
    D.append(distance(G, i)) # D[i] = distance(G, i)
  return D
  
def erdos_renyi(n, m):
  G = nx.MultiGraph(name = "erdos_renyi")
  for i in range(n):
    G.add_node(i)
  edges = []
  while len(edges) < m:
    i = random.randint(0, n - 1)
    j = random.randint(0, n - 1)
    if i != j:
      edges.append((i, j))
  G.add_edges_from(edges)
  return G
  
def configuration(degrees):
  G = nx.MultiGraph(name = "configuration")
  nodes = []
  for i in range(len(degrees)):
    G.add_node(i)
    for _ in range(degrees[i]):
      nodes.append(i)
  random.shuffle(nodes)
  edges = []
  for i in range(0, len(nodes), 2):
    edges.append((nodes[i], nodes[i + 1]))
  G.add_edges_from(edges)
  return G
  
def info(G):
  print("{:>10s} | '{:s}'".format('Graph', G.name))
  
  tic = time.time()
  n = G.number_of_nodes()
  n0, n1, delta = 0, 0, 0
  for i in G.nodes():
    if isolated(G, i):
      n0 += 1
    elif G.degree(i) == 1:
      n1 += 1
    if G.degree(i) > delta:
      delta = G.degree(i)
  
  print("{:>10s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))
  
  m = G.number_of_edges()
  m0 = nx.number_of_selfloops(G)
  
  print("{:>10s} | {:,d} ({:,d})".format('Edges', m, m0))
  print("{:>10s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))
  print("{:>10s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
      
  C = components(G)

  print("{:>10s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  
  D = distances(G, 100)
  D = [i for d in D for i in d]

  print("{:>10s} | {:.2f} ({:,d})".format('Distance', sum(D) / len(D), max(D)))
  
  if isinstance(G, nx.MultiGraph):
    G = nx.Graph(G)
    
  print("{:>10s} | {:.4f}".format('Clustering', nx.average_clustering(G)))
  
  print("{:>10s} | {:.1f} s".format('Time', time.time() - tic))
  print()

for name in ["toy", "karate_club", "collaboration_imdb", "www_google"]:
  # G = nx.Graph(nx.read_pajek("/Users/lovre/Downloads/" + name + ".net"))
  # G.name = name
  
  G = nx.Graph(name = name)
  with open("/Users/lovre/Downloads/" + name + ".net", 'r') as file:
    file.readline()
    
    for line in file:
      if line.startswith("*"):
        break
      else:
        node = line.split("\"")
        G.add_node(int(node[0]) - 1, label = node[1])
        
    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G.add_edge(i, j)
  
  info(G)
  
  info(erdos_renyi(G.number_of_nodes(), G.number_of_edges()))
  
  info(configuration([k for _, k in G.degree()]))
