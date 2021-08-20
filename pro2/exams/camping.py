import re
import requests
import matplotlib.pyplot as plt

html = requests.get("https://www.iglusport.si/taborjenje/sotori/sotori").text

prices = []
for res in re.findall(r'<span class="price">\d+,\d+', html):
  prices.append(round(float(res.split('>')[1].replace(',', '.')) / 10))

hist = [0] * (max(prices) + 1)
for price in prices:
  hist[price] += 1

fig = plt.figure()

plt.bar(range(len(hist)), hist, color = [0.5] * 3)
ticks, labels = plt.xticks()
plt.xticks(ticks = ticks, labels = [str(int(10 * tick)) for tick in ticks])
plt.xlim([0, 1.05 * max(prices)])
plt.ylim([0, 8])

plt.ylabel("Število šotorov")
plt.xlabel("Cena šotora [€]")

fig.savefig("camping.png", bbox_inches = 'tight')
