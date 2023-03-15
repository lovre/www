import random
import networkx as nx
from collections import deque

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
  return {i: sum([1 / d for d in distance(G, i)]) / (len(G) - 1) for i in G.nodes()}

def eigenvector_centrality(G, eps = 1e-6):
  E = [1] * G.number_of_nodes()
  diff = 1
  while diff > eps:
    U = [sum([E[j] for j in G[i]]) for i in G.nodes()]
    u = sum(U)
    U = [U[i] * len(G) / u for i in G.nodes()]
    diff = sum([abs(E[i] - U[i]) for i in G.nodes()])
    E = U
  return {i: E[i] for i in range(len(E))}
  
def pagerank(G, alpha = 0.85, eps = 1e-6):
  P = [1 / len(G)] * len(G)
  diff = 1
  while diff > eps:
    U = [sum([P[j] * alpha / G.degree(j) for j in G[i]]) for i in G.nodes()]
    u = sum(U)
    U = [U[i] + (1 - u) / len(G) for i in G.nodes()]
    diff = sum([abs(P[i] - U[i]) for i in G.nodes()])
    P = U
  return {i: P[i] for i in range(len(P))}

def read(name, path = "."):
  G = nx.Graph(name = name)
  with open(path + "/" + name + ".net", 'r') as file:
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
  m = G.number_of_edges()
  
  print("{:>12s} | {:,d} ({:,d})".format('Nodes', n, nx.number_of_isolates(G)))
  print("{:>12s} | {:,d} ({:,d})".format('Edges', m, nx.number_of_selfloops(G)))
  print("{:>12s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, max([k for _, k in G.degree()])))
  
  C = list(nx.connected_components(G))

  print("{:>12s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()
  
def tops(G, C, centrality, n = 15):
  print("{:>12s} | '{:s}'".format('Centrality', centrality))
  for i, c in sorted(C.items(), key = lambda item: (item[1], G.degree[item[0]]), reverse = True)[:n]:
    print("{:>12.6f} | '{:s}' ({:,d})".format(c, G.nodes[i]['label'], G.degree[i]))
  print()
  
G = read("collaboration_imdb")
  
info(G)

tops(G, {i: k / (len(G) - 1) for i, k in G.degree()}, 'degree')

tops(G, nx.clustering(G), 'clustering')
tops(G, {i: c * (G.degree(i) - 1) for i, c in nx.clustering(G).items()}, '~μ-clustering')

#tops(G, nx.eigenvector_centrality(G, tol = 1e-05), 'eigenvector')
#tops(G, nx.eigenvector_centrality_numpy(G), 'eigenvector')
tops(G, eigenvector_centrality(G), 'eigenvector')

#tops(G, nx.pagerank(G), 'pagerank')
tops(G, pagerank(G), 'pagerank')

#tops(G, nx.closeness_centrality(G), 'closeness')
tops(G, closeness_centrality(G), 'closeness')

tops(G, nx.betweenness_centrality(G), 'betweenness')
