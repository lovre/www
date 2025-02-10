import numpy as np

class Item:
  def __init__(self, name, value, weight):
    self.name = name
    self.value = value
    self.weight = weight
    
  def __repr__(self):
    return f"{self.name}({self.value}€,{self.weight}kg)"

  @staticmethod
  def value(items):
    return sum(item.value for item in items)

  @staticmethod
  def weight(items):
    return sum(item.weight for item in items)

def knapsack(items, budget):
  selected = np.empty((items.size + 1, budget + 1), dtype = object)
  for i in range(items.size + 1):
    for j in range(budget + 1):
      selected[i, j] = []

  for i in range(1, items.size + 1):
    for j in range(1, budget + 1):
      value = -1
      j_weight = j - items[i - 1].weight
      if j_weight >= 0:
        value = Item.value(selected[i - 1, j_weight]) + items[i - 1].value;

      if value >= Item.value(selected[i - 1, j]):
        selected[i, j] = selected[i - 1, j_weight] + [items[i - 1]]
      else:
        selected[i, j] = selected[i - 1, j]
        
  return selected[-1, -1]

ITEMS = np.array([Item("Green", 4, 12), Item("Gray", 2, 1),
  Item("Orange", 1, 1), Item("Blue", 2, 2), Item("Yellow", 10, 4)])
BUDGET = 15

print(f"ITEMS: {ITEMS}")
print(f"VALUE: {Item.value(ITEMS)}€")
print(f"BUDGET: {BUDGET}kg")
print()

selected = knapsack(ITEMS, BUDGET)

print(f"Optimal: {Item.value(selected)}€ / {Item.weight(selected)}kg")
print(f"Selected: {selected}")
print()
