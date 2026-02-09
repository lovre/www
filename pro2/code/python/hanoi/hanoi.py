import time

N = 7 # number of disks

def init(n = N):

  # initialize rods with all n disks on first rod

  return (list(range(n, 0, -1)), [], [])

def info(rods, n = N):

  # data structure representing rods and disks

  print(rods)
  print()

  # array representation of rods with numbers as disks

  for i in range(n - 1, -1, -1):
    for j in range(3):
      print(rods[j][i] if len(rods[j]) > i else "-", end = "")
    print()
  print()
  
  # graphic representation of rods with stars as disks
  
  for i in range(n - 1, -1, -1):
    for j in range(3):
      print(("{:" + str(n) + "s} ").format("*" * rods[j][i] if len(rods[j]) > i else ""), end = "")
    print()
  print()
  
  # pause program for 100 ms after print out
  
  time.sleep(0.1)
  
def hanoi(rods, source, destination, auxiliary, n = N):

  # move top n - 1 disks from source to auxiliary rod (using destination rod)
  
  if n > 1:
    hanoi(rods, source, auxiliary, destination, n - 1)
  
  # move last n-th disk from source to destination rod
  
  destination.append(source.pop())
  info(rods)
  
  # move top n - 1 disks from auxiliary to destination rod (using source rod)
  
  if n > 1:
    hanoi(rods, auxiliary, destination, source, n - 1)

rods = init() # initialize rods with disks

info(rods) # print out rods and disks

hanoi(rods, rods[0], rods[2], rods[1]) # move all disks from first to last rod
