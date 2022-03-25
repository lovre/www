from sklearn import *

import matplotlib.pyplot as plt

def accuracy(classes, predictions):
  """
  Compute accuracy of predicted classes relative to true classes.
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
  plt.title(data.target[i], fontsize = 8)
  plt.axis('off')

fig.savefig("digits.pdf", bbox_inches = 'tight')
plt.close(fig)

# initializes classification models in scikit-learn library

classifiers = {"kNN": neighbors.KNeighborsClassifier(), "NB": naive_bayes.GaussianNB(), "DT": tree.DecisionTreeClassifier(), "RF": ensemble.RandomForestClassifier(), "SVM": svm.SVC(), "MLP": neural_network.MLPClassifier(), "SGD": linear_model.SGDClassifier()}

# defines instance values and true classes of handwritten digits

instances = data.data
classes = data.target

# splits data into 80% train instances and 20% test instances

n = len(instances)

train_instances = instances[n // 5:]
train_classes = classes[n // 5:]

test_instances = instances[:n // 5]
test_classes = classes[:n // 5]

# prints out accuracy of classification models on handwritten digits

print("   Model | Accuracy")

for name, classifier in classifiers.items():
  classifier.fit(train_instances, train_classes)
  
  test_predictions = classifier.predict(test_instances)

  print("{:>8s} |  {:5.2f}%".format("'" + name + "'", 100 * accuracy(test_classes, test_predictions)))
