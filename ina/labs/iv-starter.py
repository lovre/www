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
  
def info(G):
  print("{:>10s} | '{:s}'".format('Graph', G.name))

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
      
  C = components(G)

  print("{:>10s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()

for name in ["toy", "karate_club", "collaboration_imdb", "www_google"]:
#  G = nx.Graph(nx.read_pajek("./" + name + ".net"))
#  G = nx.convert_node_labels_to_integers(G, label_attribute = 'label')
#  G.name = name
  
  G = nx.Graph(name = name)
  with open("./" + name + ".net", 'r') as file:
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
