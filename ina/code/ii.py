
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
  N = set(range(len(G)))
  while N:
    C.append(component(G, N, next(iter(N))))
  return C

for name in ["toy", "karate_club", "www_google"]:
  G, n, m = None, 0, 0
  with open("/Users/lovre/Downloads/" + name + ".net", 'r') as file:
    n = int(file.readline().split()[1])
    G = [[] for _ in range(n)]

    for line in file:
      if line.startswith("*"):
        break
    
    m = 0
    for line in file:
      i, j = (int(x) - 1 for x in line.split()[:2])
      G[i].append(j)
      G[j].append(i)
      m += 1
  
  n0, n1, delta = 0, 0, 0
  for i in range(n):
    if isolated(G, i):
      n0 += 1
    elif len(G[i]) == 1:
      n1 += 1
    if len(G[i]) > delta:
      delta = len(G[i])
      
  C = components(G)

  print("{:>10s} | '{:s}'".format('Graph', name))
  print("{:>10s} | {:,d} ({:,d}, {:,d})".format('Nodes', n, n0, n1))
  print("{:>10s} | {:,d}".format('Edges', m))
  print("{:>10s} | {:.2f} ({:,d})".format('Degree', 2 * m / n, delta))
  print("{:>10s} | {:.2e}".format('Density', 2 * m / n / (n - 1)))
  print("{:>10s} | {:.1f}% ({:,d})".format('LCC', 100 * max(len(c) for c in C) / n, len(C)))
  print()
