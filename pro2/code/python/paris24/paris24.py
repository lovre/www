import requests
import matplotlib.pyplot as plt

data = requests.get("https://lovro.fri.uni-lj.si/api/paris24").json()

results = []
for country in data:
  medals = data[country]['gold'] + data[country]['silver'] + data[country]['bronze']
  results.append((country, medals, medals / data[country]['population'] * 10**6))

fig, axs = plt.subplots(1, 2, figsize = [15.6, 4.8])

results.sort(key = lambda item: item[1])
axs[0].barh([c for c, _, _ in results[-20:]], [r for _, r, _ in results[-20:]], color = '0.9', ec = 'k')
axs[0].title.set_text("Število medalj")

results.sort(key = lambda item: item[2])
axs[1].barh([c for c, _, _ in results[-20:]], [r for _, _, r in results[-20:]], color = '0.9', ec = 'k', log = True)
axs[1].title.set_text("Število medalj / milijon prebivalcev")

fig.savefig("paris24.pdf", bbox_inches = 'tight')
