
def fib(n):
  if n <= 1:
    return n
  else:
    return fib(n - 1) + fib(n - 2)

def fib(n):
  nums = [0, 1]
  for i in range(2, n + 1):
    nums.append(nums[i - 1] + nums[i - 2])
  return nums[n]
    
for i in range(100):
  print("F({:d}) = {:,d}".format(i, fib(i)))
