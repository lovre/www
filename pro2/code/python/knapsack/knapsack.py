
class Item:

  def __init__(self, name, value, weight):
    self.name = name
    self.value = value
    self.weight = weight

items = []
items.append(Item("green", 4, 12))
items.append(Item("gray", 2, 1))
items.append(Item("yellow", 10, 4))
items.append(Item("orange", 1, 1))
items.append(Item("blue", 2, 2))

def knapsack(items, budget):
  values = [[0] * (budget + 1) for _ in range(len(items) + 1)]
  
  for i in range(1, len(items) + 1):
    for j in range(1, budget + 1):
      value = -1
      if j - items[i - 1].weight >= 0:
        value = values[i - 1][j - items[i - 1].weight] + items[i - 1].value;
        
      if values[i - 1][j] >= value:
        values[i][j] = values[i - 1][j]
      else:
        values[i][j] = value

  return values[-1][-1]

print(knapsack(items, 15))
