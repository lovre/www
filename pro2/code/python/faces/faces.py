import os
import numpy as np

import matplotlib.image as im

faces = []
for name in os.listdir('faces'):
  if name.endswith('.png'):
    face = im.imread(os.path.join('faces', name))
    faces.append(face)
    
h, w, c = faces[0].shape
img = np.zeros((h, w, c))

for i in range(h):
  for j in range(w):
#    for k in range(c):
#      for face in faces:
#        img[i][j][k] += face[i][j][k] / len(faces)

#    for face in faces:
#      img[i][j] += face[i][j] / len(faces)
    
    img[i][j] = np.average([face[i][j] for face in faces], axis = 0)

im.imsave('face.png', img)
