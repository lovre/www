import math
from sklearn import *
import matplotlib.pyplot as plt

def accuracy(classes, predictions):
  """
  Compute accuracy of predicted classes to true classes.
  """
  
  count = 0
  for i in range(len(classes)):
    if classes[i] == predictions[i]:
      count += 1
      
  return count / len(classes)

# reads handwritten digits from scikit-learn repository

data = datasets.load_digits()

# plots first 192 digits and stores image to PDF file

fig = plt.figure()

for i in range(192):
  plt.subplot(8, 24, i + 1)

  plt.imshow(data.images[i], cmap = 'binary')
  plt.title(data.target[i], fontsize = 5)
  plt.axis('off')

fig.savefig("digits.pdf", bbox_inches = 'tight')
plt.close(fig)

# initializes classification models from scikit-learn library

classifiers = {"kNN": neighbors.KNeighborsClassifier(), "DT": tree.DecisionTreeClassifier(), "RF": ensemble.RandomForestClassifier(), "SVM": svm.SVC(), "MLP": neural_network.MLPClassifier()}

# defines instances, images and true classes of handwritten digits

instances = data.data
images = data.images
classes = data.target

# splits data into 90% train instances and 10% test instances

n = len(instances)
k = int(0.9 * n)

train_instances = instances[:k]
train_images = images[:k]
train_classes = classes[:k]

test_instances = instances[k:]
test_images = images[k:]
test_classes = classes[k:]

# prints out accuracy of classification models on handwritten digits

for name, classifier in classifiers.items():
  classifier.fit(train_instances, train_classes)
  
  test_predictions = classifier.predict(test_instances)

  print("{:5.1f}% | {:s} ".format(100 * accuracy(test_classes, test_predictions), name))

# predictions of selected classification model on handwritten digits

classifier = classifiers["kNN"]

classifier.fit(train_instances, train_classes)

test_predictions = classifier.predict(test_instances)

# plots prediction errors on test digits and stores image to PDF file

fig = plt.figure()

for i in range(n - k):
  plt.subplot(8, math.ceil((n - k) / 8), i + 1)

  plt.imshow(test_images[i], cmap = 'binary')
  if test_classes[i] != test_predictions[i]:
    plt.title(r"$" + str(test_classes[i]) + "\\neq " + str(test_predictions[i]) + "$", fontsize = 5)
  plt.axis('off')

fig.savefig("errors.pdf", bbox_inches = 'tight')
plt.close(fig)
