import operator as op

def edit_dist(fst, snd):
  """
  Compute Levenshtein or edit distance between given two strings.
  Function returns number of operations needed to traverse one string to another.
  """
  
  dists = [[0 for _ in range(len(snd) + 1)] for _ in range(len(fst) + 1)]
  
  for i in range(len(fst) + 1):
    dists[i][0] = i
  for j in range(len(snd) + 1):
    dists[0][j] = j
    
  for j in range(1, len(snd) + 1):
    for i in range(1, len(fst) + 1):
      dists[i][j] = min(dists[i - 1][j - 1] if fst[i - 1] == snd[j - 1] else dists[i - 1][j - 1] + 1, dists[i - 1][j] + 1, dists[i][j - 1] + 1)
      
  return dists[len(fst)][len(snd)]

# create list of character names in GoT network

got = []
with open('got_kills.net', 'r') as file:
  for line in file:
    if line.startswith('*vertices'):
      continue
    elif line.startswith('*edges'):
      break
    else:
      got.append(line.split('"')[1].split(' - ')[0].strip())

got.sort()

# compute (relative) edit distance between character names

dists = []
for fst in got:
  for snd in got:
    if fst < snd:
      dist = edit_dist(fst, snd) / max(len(fst), len(snd))
      dists.append((fst, snd, dist))

dists = sorted(dists, key = lambda item: item[2])

# print out most similar character names in GoT network

for i in range(10):
  fst, snd, dist = dists[i]
  print("{:9.6f} | '{:s}' ≈ '{:s}'".format(dist, fst, snd))
