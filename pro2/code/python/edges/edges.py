import numpy as np
import matplotlib.image as im

MASK = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

img = im.imread('picture.png')

h, w, _ = img.shape
for i in range(h):
  for j in range(w):
    img[i][j][:3] = sum(img[i][j][:3]) / 3

edg = np.ones((h, w, 3))

for i in range(1, h - 1):
  for j in range(1, w - 1):
    pixels = img[i - 1:i + 2, j - 1:j + 2, 0]
    hor = abs((MASK * pixels).sum()) / 4
    ver = abs((np.transpose(MASK) * pixels).sum()) / 4
    edg[i][j] = 1 - (hor + ver) / 2

thres = np.sort(edg.flatten())[edg.size // 8]

for i in range(h):
  for j in range(w):
    edg[i][j] = 0 if edg[i][j][0] < thres else 1

im.imsave('edges.png', edg)
