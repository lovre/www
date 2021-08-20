import random

numbers = set()
while len(numbers) < 10**6:
  numbers.add(random.randint(0, 10**12))
number = list(numbers)

#for c in range(5):
#  for n in numbers:
#    if n % 2 == 0:
#      i = 0
#      for m in numbers:
#        if m > n and m % 2 == 0:
#          i += 1
#      if i == c:
#        print(n)
#        break

def maxeven(numbers):
  m = -1
  for n in numbers:
    if n % 2 == 0 and n > m:
      m = n
  numbers.remove(m)
  print(m)

for _ in range(8):
  maxeven(numbers)
