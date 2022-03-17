import re
import time
import json
import operator

def edit_dist(fst, snd):
  dist = [[0] * (len(snd) + 1) for _ in range(len(fst) + 1)]
  for i in range(len(fst) + 1):
    dist[i][0] = i
  for j in range(len(snd) + 1):
    dist[0][j] = j
  for i in range(1, len(fst) + 1):
    for j in range(1, len(snd) + 1):
      dist[i][j] = min(dist[i - 1][j - 1] if fst[i - 1] == snd[j - 1] else dist[i - 1][j - 1] + 1, dist[i - 1][j] + 1, dist[i][j - 1] + 1)
  return dist[len(fst)][len(snd)]

def is_valid(word):
  if "." in word:
    return False
  if re.match(GREEN.replace(".", "[^" + GRAY + "]") if len(GRAY) > 0 else GREEN, word) == None:
    return False
  for char in YELLOW:
    if len({ind.start() for ind in re.finditer(char, word)}.difference(YELLOW[char])) == 0:
      return False
  return True
  
def count_new(word):
  new = set(word).difference(set(GREEN))
  return len(new.difference(YELLOW.keys()))

# Besedle 877 for AUDIO

GREEN = ".U..."
GRAY = "DIO"
YELLOW = {}
YELLOW["A"] = {0}

print("\n   GREEN | '{:s}'".format(GREEN))
print("    GRAY | '{:s}'".format(GRAY))
print("  YELLOW | {:s}".format(str(YELLOW)))

# ADIEU, AUDIO = starts with 4 different vowels

besedle = json.load(open('besedle.json'))

for word in list(besedle.keys()):
  if not is_valid(word):
    besedle.pop(word)

words = sorted(besedle.keys())

print("\n   Words | {:,d}".format(len(words)))
print("         | {:s}".format(str(words)[:2500] + ("..." if len(str(words)) > 2500 else "")))

tic = time.time()

# VIDEO, LITER, START = most frequent words on Google

print("\n         | # | Google (new)")
for i, (word, hits) in enumerate(sorted(besedle.items(), key = operator.itemgetter(1), reverse = True)):
  if i >= 8:
    break
  print("{:>8s} | {:d} | {:,d} ({:d})".format(word, i + 1, hits, count_new(word)))
  
# SOLEA = word with minimum average edit distance

dists = {}
for word in words:
  dist = 0
  for other in words:
    dist += edit_dist(word, other)
  dists[word] = 0 if dist == 0 else dist / (len(words) - 1)

print("\n         | # | Close (new)")
for i, (word, dist) in enumerate(sorted(dists.items(), key = operator.itemgetter(1))):
  if i >= 8:
    break
  print("{:>8s} | {:d} | {:.3f} ({:d})".format(word, i + 1, dist, count_new(word)))

print("\n    Time | {:.1f} sec\n".format(time.time() - tic))
