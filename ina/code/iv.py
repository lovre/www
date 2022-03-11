import time
import random
import operator
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
  D = [-1] * len(G)
  Q = deque()
  D[i] = 0
  Q.append(i)
  while Q:
    i = Q.popleft()
    for j in G[i]:
      if D[j] == -1:
        D[j] = D[i] + 1
        Q.append(j)
  return [d for d in D if d > 0]

def closeness_centrality(G):
  return {i: sum([1 / d for d in distance(G, i)]) / (G.number_of_nodes() - 1) for i in G.nodes()}

def eigenvector_centrality(G, eps = 1e-6):
  E = [1] * G.number_of_nodes()
  diff = 1
  while diff > eps:
    U = [sum([E[j] for j in G[i]]) for i in G.nodes()]
    u = sum(U)
    U = [U[i] * G.number_of_nodes() / u for i in G.nodes()]
    diff = sum([abs(E[i] - U[i]) for i in G.nodes()])
    E = U
  return {i: E[i] for i in range(len(E))}
  
def pagerank(G, alpha = 0.85, eps = 1e-6):
  P = [1 / G.number_of_nodes()] * G.number_of_nodes()
  diff = 1
  while diff > eps:
    U = [sum([P[j] * alpha / G.degree(j) for j in G[i]]) for i in G.nodes()]
    u = sum(U)
    U = [U[i] + (1 - u) / G.number_of_nodes() for i in G.nodes()]
    diff = sum([abs(P[i] - U[i]) for i in G.nodes()])
    P = U
  return {i: P[i] for i in range(len(P))}

def read(name):
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
      
  return G
  
def info(G):
  print("{:>12s} | '{:s}'".format('Graph', G.name))

  n = G.number_of_nodes()
  n0, n1, delta = 0, 0, 0
  for i in G.nodes():
    if isolated(G, i):
      n0 += 1
    elif G.degree(i) == 1:
      n1 += 1
    if G.degree(i) > delta:
      delta = G.degree(i)
  
  print("{:>12s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))
  
  m = G.number_of_edges()
  m0 = nx.number_of_selfloops(G)
  
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, m0))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))
  print("{:>12s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
      
  C = components(G)

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()
  
def tops(G, centrality, label, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', label))
  
  tic = time.time()
  C = centrality(G)
  
  for p, (i, c) in enumerate(sorted(C.items(), key = operator.itemgetter(1), reverse = True)):
    if p < n:
      print("{:>12.6f} | '{:s}' ({:,d})".format(c, G.nodes[i]['label'], G.degree[i]))
      
  print("{:>12s} | {:.1f} s".format('Time', time.time() - tic))
  print()
  
G = read("collaboration_imdb")
  
info(G)

tops(G, lambda G: {i: G.degree(i) / (G.number_of_nodes() - 1) for i in G.nodes()}, 'degree')

tops(G, nx.clustering, 'clustering')

tops(G, lambda G: {i: c * (G.degree(i) - 1) for i, c in nx.clustering(G).items()}, '~μ-clustering')

tops(G, closeness_centrality, 'closeness')
#tops(G, nx.closeness_centrality, 'closeness')

tops(G, nx.betweenness_centrality, 'betweenness')

tops(G, eigenvector_centrality, 'eigenvector')
#tops(G, nx.eigenvector_centrality_numpy, 'eigenvector')
#tops(G, lambda G: nx.eigenvector_centrality(G, tol = 1e-05), 'eigenvector')

tops(G, pagerank, 'pagerank')
#tops(G, nx.pagerank, 'pagerank')
