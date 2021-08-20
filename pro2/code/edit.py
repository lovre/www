import operator as op

def edit_dist(fst, snd):
  """
  Compute Levenshtein or edit distance between given two strings.
  Function returns number of operations needed to traverse one string to another.
  """
  dist = [[0 for _ in range(len(snd) + 1)] for _ in range(len(fst) + 1)]
  for i in range(len(fst) + 1):
    dist[i][0] = i
  for j in range(len(snd) + 1):
    dist[0][j] = j
  for j in range(1, len(snd) + 1):
    for i in range(1, len(fst) + 1):
      dist[i][j] = min(dist[i - 1][j - 1] if fst[i - 1] == snd[j - 1] else dist[i - 1][j - 1] + 1, dist[i - 1][j] + 1, dist[i][j - 1] + 1)
  return dist[len(fst)][len(snd)]

# creates list of names of characters in GoT network

chars = []
with open('got_kills.net', 'r') as file:
  for line in file:
    if line.startswith('*vertices'):
      continue
    elif line.startswith('*edges'):
      break
    else:
      chars.append(line.split('"')[1].split(' - ')[0].strip())
chars.sort()

# prints out most similar GoT characters due to edit distance

for char in chars:
  dist = {}
  for other in chars:
    if char != other:
      dist[other] = edit_dist(char, other)
  print("{:>30s} | {:s}".format("Character", "Like '" + char + "'"))
  for i, (other, d) in enumerate(sorted(dist.items(), key = op.itemgetter(1))):
    if i < 5:
      print("{:>30s} | {:4.1f}% ({:d} ops)".format("'" + other + "'", 100 * (1 - d / max(len(char), len(other))), d))
  print()
