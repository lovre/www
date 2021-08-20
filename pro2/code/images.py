import os
import random

import numpy as np
import matplotlib.image as im
import matplotlib.pyplot as plt

from networks import Graph

def read_image(name, path = '.'):
  """
  Read bitmap image from the specified file in PNG format.
  Function returns NumPy array of arrays storing RGB values of pixels.
  """
  return im.imread(os.path.join(path, name + '.png'))

def save_image(img, name, path = '.'):
  """
  Write bitmap image to the specified file in PNG format.
  Method also creates the specified folder if it doesn't exist.
  """
  if not os.path.exists(path):
    os.makedirs(path)
  
  fig = plt.figure()
  plt.axis('off')

  plt.imshow(img)

  fig.savefig(os.path.join(path, name + '.png'), bbox_inches = 'tight')
  plt.close(fig)
  
def grayscale_image(img):
  """
  Create grayscale bitmap image from the specified color bitmap image.
  Function returns NumPy array of arrays storing RGB values of pixels.
  """
  gs = np.ones(img.shape)
  
  for i in range(img.shape[0]):
    for j in range(img.shape[1]):
      gs[i][j][:3] = sum(img[i][j][:3]) / 3

  return gs
  
def inverted_image(img):
  """
  Create inverted bitmap image from the specified color bitmap image.
  Inverted image assigns black (white) color to white (non-white) pixels of color image.
  Function returns NumPy array of arrays storing RGB values of pixels.
  """
  inv = np.ones(img.shape)
  
  for i in range(img.shape[0]):
    for j in range(img.shape[1]):
      if np.prod(img[i][j]) == 1:
        inv[i][j] = [0, 0, 0, 1]

  return inv
  
def corrected_image(img):
  """
  Create corrected bitmap image from the specified black & white bitmap image.
  Corrected image assigns white color to black pixels surrounded by only black pixels.
  Function returns NumPy array of arrays storing RGB values of pixels.
  """
  corr = np.copy(img)
  
  for i in range(1, img.shape[0] - 1):
    for j in range(1, img.shape[1] - 1):
      if np.sum(img[i - 1:i + 2, j - 1:j + 2, :3]) == 0:
        corr[i][j] = [1, 1, 1, 1]

  return corr

def image2graph(img, name = 'graph', eps = 0.033):
  """
  Create graph from the specified color bitmap image, where nodes are pixels
  and edges represent adjacent pixels whose RGB distance is smaller than eps.
  Function returns simple undirected graph represented by class Graph.
  """
  G = Graph(name)
  (h, w) = img.shape[:2]
  
  for i in range(h):
    for j in range(w):
      G.add_node()

  for i in range(h):
    for j in range(w):
      if j + 1 < w and np.linalg.norm(img[i][j] - img[i][j + 1]) < eps: # right
        G.add_edge(i * w + j, i * w + j + 1)
      if i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j]) < eps: # down
        G.add_edge(i * w + j, (i + 1) * w + j)
      if j + 1 < w and i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j + 1]) < eps: # down right
        G.add_edge(i * w + j, (i + 1) * w + j + 1)
      if j - 1 >= 0 and i + 1 < h and np.linalg.norm(img[i][j] - img[i + 1][j - 1]) < eps: # down left
        G.add_edge(i * w + j, (i + 1) * w + j - 1)

  return G
  
def graph2segmented(G, C, shape, eps = 0.005):
  """
  Create segmented bitmap image from the specified graph and node clustering.
  Segmented image assigns same random color to pixels corresponding to nodes in each cluster.
  Function returns NumPy array of arrays storing RGB values of pixels.
  """
  seg = np.ones(shape)
  (h, w) = img.shape[:2]
  
  for c in C:
    clr = [random.random() for _ in range(3)] if len(c) > eps * G.get_n() else [1, 1, 1]
    for i in c:
      seg[i // w][i % w][:3] = clr

  return seg
  
for name in os.listdir('figs'):
  if name.endswith('.png'):
    name = name[:-4]

    # reads color bitmap image from PNG file

    img = read_image(name, 'figs')
    
    # creates grayscale image from color image

    #gs = grayscale_image(img)
   
    # creates undirected graph from color image

    G = image2graph(img, name)
    
    print(G)
    
    # creates segmented image from graph's connected components

    seg = graph2segmented(G, Graph.components(G), img.shape)

    # creates inverted image from segmented image

    inv = inverted_image(seg)

    # corrects black patches of inverted image

    corr = corrected_image(inv)
    
    # creates coloring of original color image

    clr = np.concatenate([img, np.ones([img.shape[0], img.shape[1] // 10, 4]), corr], axis = 1)
    
    save_image(clr, name, 'outs')
