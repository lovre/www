import os
  
def orbit_counts(G, size = 4):
  with open(G.name + ".in", 'w') as file:
    file.write(str(G.number_of_nodes()) + " " + str(G.number_of_edges()) + "\n")
    for edge in G.edges():
      file.write(str(edge[0]) + " " + str(edge[1]) + "\n")

  os.system("./orca node " + str(size) + " " + G.name + ".in " + G.name + ".orca")
  
  orbits = []
  with open(G.name + ".orca", 'r') as file:
    for line in file:
      orbits.append([int(k) for k in line.split()])
  
  os.remove(G.name + ".in")
  os.remove(G.name + ".orca")

  return orbits
  
def orbit_distributions(orbits):
  dists = []
  
  for o in range(len(orbits[0])):
    pk = {}
    for i in range(len(orbits)):
      k = orbits[i][o]
      if k not in pk:
        pk[k] = 0
      pk[k] += 1 / k if k > 0 else 0
    p = sum(pk.values())
    
    dists.append({k: pk[k] / p if p > 0 else pk[k] for k in pk})
    
  return dists
  
def graphlet_disaggrement(G1, G2, size = 4):
  P = orbit_distributions(orbit_counts(G1, size = size))
  Q = orbit_distributions(orbit_counts(G2, size = size))
  
  A = 0
  for o in range(len(P)):
    a = 0
    for k in set.union(set(P[o].keys()), Q[o].keys()):
      p = P[o][k] if k in P[o] else 0
      q = Q[o][k] if k in Q[o] else 0
      a += (p - q) ** 2
      
    A += 1 - (a / 2) ** 0.5
    
  return 1 - A / len(P)
