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

# reads electricity consumption of Ljubljana from ARFF file

data = []
with open("electricity.arff", 'r') as file:
  for line in file:
    if line.startswith("@data"):
      break

  for line in file:
    if '?' not in line:
      values = [float(val) if i > 0 else datetime.strptime(val, '"%m/%d/%y %H:%M"') for i, val in enumerate(line.split(','))]
      data.append(values)

# plots first two weeks of electricity consumption and stores image to PDF file

datetimes = [instance[0] for instance in data[:14 * 24]]
electricity = [instance[-1] for instance in data[:14 * 24]]

fig = plt.figure()

plt.plot(datetimes, electricity)

plt.ylim(0, 1.25 * max(electricity))
plt.xticks([datetimes[i * len(datetimes) // 6] for i in range(6)] + [datetimes[-1]], fontsize = 6)

fig.savefig("electricity.pdf", bbox_inches = 'tight')
plt.close(fig)

# initializes regression models from scikit-learn library

regressors = {"kNN": neighbors.KNeighborsRegressor(), "LR": linear_model.LinearRegression(), "RF": ensemble.RandomForestRegressor(), "SVM": svm.SVR()}

# defines data instances and true values of electricity consumption

instances = [[instance[0].timestamp()] + instance[1:-1] for instance in data]
values = [instance[-1] for instance in data]

## splits data into 92% train instances (eleven months) and 8% test instances (last month)

k = 30 * 24

train_instances = instances[:-k]
train_values = values[:-k]

test_instances = instances[-k:]
test_values = values[-k:]

# prints out MAPE of regression models on electricity consumption

for name, regressor in regressors.items():
  regressor.fit(train_instances, train_values)
  
  test_predictions = regressor.predict(test_instances)

  print("{:5.1f}% | {:s}".format(100 * MAPE(test_values, test_predictions), name))

# predictions of selected regression model on electricity consumption

regressor = regressors["RF"]

regressor.fit(train_instances, train_values)

test_predictions = regressor.predict(test_instances)

# plots prediction on first half of test instances and stores image to PDF file

k = len(test_values) // 2

fig = plt.figure()

plt.plot(range(k), test_values[:k], label = "Consumption")
plt.plot(range(k), test_predictions[:k], label = "Prediction")

plt.ylim(0, 1.25 * max(test_values[:k]))
plt.xticks([])
plt.legend()

fig.savefig("errors.pdf", bbox_inches = 'tight')
plt.close(fig)
