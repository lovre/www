import numpy as np
import matplotlib.image as im

img = im.imread('painting.png')

for i in range(img.shape[0] // 4):
  for j in range(img.shape[1] // 4):
    clr = np.average([img[4 * i + x][4 * j + y] \
      for x in range(4) for y in range(4)], axis = 0)
    for x in range(4):
      for y in range(4):
        img[4 * i + x][4 * j + y] = clr

im.imsave('granular.png', img)
