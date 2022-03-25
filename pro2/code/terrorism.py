import random

import numpy as np

from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

def normalize(data):
  """
  Compute standard normalized values of given data instances.
  Function returns distances from mean in units of standard deviation.
  """
  means, stds = [0] * len(data[0]), [0] * len(data[0])
  for j in range(len(means)):
    values = [data[i][j] for i in range(len(data))]
    means[j], stds[j] = np.mean(values), np.std(values)

  for i in range(len(data)):
    for j in range(len(data[i])):
      data[i][j] = (data[i][j] - means[j]) / stds[j]

  return data

def k_means(data, k = 3):
  """
  Cluster data instances into k clusters using k-means algorithm.
  Function returns clusters of data instances and locations of centroids.
  """
  n = len(data)
  clusters = [0] * n
  
  centroids = np.array(random.choices(data, k = k))

  for _ in range(100):
    stopping = True

    for i in range(n):
      distance = np.linalg.norm(data[i] - centroids[clusters[i]])

      for c in range(k):
        d = np.linalg.norm(data[i] - centroids[c])

        if d < distance:
          distance = d
          clusters[i] = c
          stopping = False

    if stopping:
      break

    for c in range(k):
      centroids[c] = np.average([data[i] for i, cluster in enumerate(clusters) if cluster == c], axis = 0)

  return clusters, centroids

# reads data on terrorism attacks from TSV file

data, attributes = [], None
with open("terrorism.tab", 'r') as file:
  attributes = file.readline().strip().split('\t')[1:]
  
  for line in file:
    data.append([float(value) for value in line.split('\t')[1:]])

# stores latitudes, longitudes and views of terrorism attacks

latitudes = [instance[1] for instance in data]
longitudes = [instance[2] for instance in data]

views = [instance[-1] for instance in data]

# clusters terrorism attacks using k-means algorithm

data = normalize(data)

clusters, centroids = k_means(data, 3)

# plots clustering of terrorism attacks as colored map

fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12.8, 4.8))

map = Basemap(ax = ax1)
map.drawcoastlines()
# map.fillcontinents()
# map.bluemarble()

ax1.scatter(longitudes, latitudes, zorder = 2, marker = '*', \
  s = [50 + v**0.5 / 2 for v in views], c = clusters, cmap = 'viridis', edgecolors = ['black'])

ax1.set_ylim(10, 67.5)
ax1.set_xlim(-12.5, 60)

# plots clusters of terrorism attacks as bar chart

cmap = cm.get_cmap('viridis')
width = 1 / (len(centroids) + 1)

for i, centroid in enumerate(centroids):
  ax2.barh([i * width + j for j in range(len(centroid))], centroid, width, \
    color = cmap(i / (len(centroids) - 1)), edgecolor = 'black')

ax2.plot([0, 0], [-1, len(attributes)], c = 'black', linewidth = 1)

ax2.set_xticks([])
ax2.set_yticks([j + width for j in range(len(attributes))])
ax2.set_yticklabels(attributes)
ax2.set_ylim(-1.5 * width, len(attributes))

fig.savefig("terrorism.pdf", bbox_inches = 'tight')
plt.close(fig)
