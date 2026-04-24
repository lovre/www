
import networkx as nx
from math import log, sqrt

def pdf(G, i):
  P = [0] * len(G)
  for j in nx.single_source_shortest_path_length(G, i).values():
    P[j] += 1 / G.number_of_nodes()
  return P

def pdfs(G):
  return [pdf(G, i) for i in G.nodes()]

def mu(Ps):
  return [sum(P[j] for P in Ps) / len(Ps) for j in range(len(Ps[0]))]
  
def jensen_shannon(Ps, M):
  return sum(Ps[i][j] * log(Ps[i][j] / M[j]) for j in range(len(M)) for i in range(len(Ps)) if Ps[i][j] > 0) / len(Ps)

def node_dispersion(Ps, M):
  return jensen_shannon(Ps, M) / log(M.index(0) + 1)
  
def node_distances(M1, M2):
  if len(M1) < len(M2):
    M2 = M2[:len(M1)]
  elif len(M1) > len(M2):
    M1 = M1[:len(M2)]
  return jensen_shannon([M1, M2], mu([M1, M2]))

def simplified_dmeasure(Ps1, M1, Ps2, M2):
  return (sqrt(node_distances(M1, M2) / log(2)) + abs(sqrt(node_dispersion(Ps1, M1)) - sqrt(node_dispersion(Ps2, M2)))) / 2

def dmeasure(G1, G2):
  Ps1 = pdfs(G1)
  Ps2 = pdfs(G2)
  return simplified_dmeasure(Ps1, mu(Ps1), Ps2, mu(Ps2))
