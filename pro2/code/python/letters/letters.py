import os
import matplotlib.pyplot as plt

ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def frequency(text):
  freq = {c: 0 for c in ALPHABET}

  for c in text.lower():
    if c in ALPHABET:
      freq[c] += 1
          
  s = sum(freq.values())
  for c in ALPHABET:
    freq[c] /= s

  return freq

fig = plt.figure()

for name in os.listdir("."):
  if name.endswith(".txt"):
    with open(name, 'r') as file:
      freq = frequency(file.read())
    
      plt.plot(list(ALPHABET), [freq[c] for c in ALPHABET], label = name)

plt.ylabel("Relative frequency")
plt.legend()

fig.savefig("letters.pdf", bbox_inches = 'tight')
