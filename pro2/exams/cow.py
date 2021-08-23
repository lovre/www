import requests

labels, freqs = [], {}
for line in requests.get("https://lovro.lpt.fri.uni-lj.si/api/cow").text.split('\n'):
  line = line.strip()
  if line.startswith('*vertices'):
    pass
  elif line.startswith('*edges'):
    freqs = {label: 0 for label in labels}
  elif '"' in line:
    labels.append(line.split('"')[1])
  else:
    for ind in line.split():
      freqs[labels[int(ind) - 1]] += 1

with open("cow.txt", 'w') as file:
  for label, freq in sorted(freqs.items(), key = lambda item: item[1], reverse = True):
    file.write(label + '\t' + str(freq) + '\n')
