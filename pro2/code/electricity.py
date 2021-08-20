from datetime import *

import numpy as np
from sklearn import *

import matplotlib.pyplot as plt

def MAPE(values, predictions):
  """
  Compute mean absolute percentage error between predicted and true values.
  """
  error = 0
  for i in range(len(values)):
    if values[i] > 0:
      error += abs((values[i] - predictions[i]) / values[i])
  return error / len(values)

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

# reads electricity consumption of Ljubljana from ARFF file

data = []
with open("electricity.arff", 'r') as file:
  for line in file:
    if line.startswith("@data"):
      break
  for line in file:
    if '?' not in line:
      data.append([float(value) if i > 0 else datetime.strptime(value, '"%m/%d/%y %H:%M"') for i, value in enumerate(line.split(','))])

# plots first two weeks of electricity consumption and stores image to PDF file

datetimes = [instance[0] for instance in data[:14 * 24]]
electricity = [instance[-1] for instance in data[:14 * 24]]

fig = plt.figure()

plt.fill_between(datetimes, electricity, color = [0, 0, 0], alpha = 0.33)

plt.ylim(0, 1.25 * max(electricity))
plt.xlim(datetimes[0], datetimes[-1])
plt.xticks([datetimes[i * len(datetimes) // 5] for i in range(5)])

plt.title("Ljubljana electricity consumption", fontweight = 'bold')
plt.ylabel("Electricity consumption")
plt.xlabel("Date and time")

fig.savefig("electricity.pdf", bbox_inches = 'tight')
plt.close(fig)

# initializes regression models in scikit-learn library

regressors = {"kNN": neighbors.KNeighborsRegressor(), "LR": linear_model.LinearRegression(), "DT": tree.DecisionTreeRegressor(), "RF": ensemble.RandomForestRegressor(max_depth = 20, n_estimators = 50), "SVM": svm.SVR(gamma = 'scale'), "MLP": neural_network.MLPRegressor(max_iter = 2000)}

# defines data instances and true values of electricity consumption

instances = normalize([[instance[0].timestamp()] + instance[1:-1] for instance in data])
values = [instance[-1] for instance in data]

## splits data into train instances (first weeks) and test instances (last week)

train_instances = instances[:-7 * 24]
train_values = values[:-7 * 24]

test_instances = instances[-7 * 24:]
test_values = values[-7 * 24:]

# prints out MAPE of regression models on electricity consumption

print("   Model |  MAPE")

for name, regressor in regressors.items():
  regressor.fit(train_instances, train_values)
  
  test_predictions = regressor.predict(test_instances)

  print("{:>8s} | {:5.2f}%".format("'" + name + "'", 100 * MAPE(test_values, test_predictions)))

