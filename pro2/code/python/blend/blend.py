import numpy as np

import matplotlib.image as im

img1 = im.imread('tree1.png')
img2 = im.imread('tree2.png')

img = np.ones(img1.shape)

h, w, _ = img.shape
for i in range(h):
  for j in range(w):
    if j < w / 3:
      alpha = 0
    elif j >= 2 * w / 3:
      alpha = 1
    else:
      alpha = 3 * j / w - 1
    img[i][j] = (1 - alpha) * img1[i][j] + alpha * img2[i][j]

im.imsave('tree.png', img)
