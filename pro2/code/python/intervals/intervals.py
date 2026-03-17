
class Interval:
  """
  Class storing closed interval represented by lower and upper bound.
  """
  
  def __init__(self, lower = 0, upper = 1):
    if lower > upper:
      raise Exception("lower bound {:} is larger than upper bound {:}".format(lower, upper))
      
    self.lower = lower
    self.upper = upper
    
  def __str__(self):
    return "[{:}, {:}]".format(self.lower, self.upper)
    
  def __repr__(self):
    return "Interval({:}, {:})".format(self.lower, self.upper)
    
  def __len__(self):
    return self.upper - self.lower
    
  def __add__(self, interval):
    return Interval(min(self.lower, interval.lower), max(self.upper, interval.upper))
  
  def includes(self, arg):
    if type(arg) is int or type(arg) is float:
      return arg >= self.lower and arg <= self.upper
    elif type(arg) is Interval:
      return arg.lower >= self.lower and arg.upper <= self.upper
    else:
      raise Exception("unsupported argument type {:}".format(type(arg)))
  
a = Interval(2, 7)

print(a)
print(repr(a))
print(len(a))

b = Interval(5, 9)
c = Interval(-3, 0)

print(a + b)
print(a + c)

print(a.includes(1))
print(a.includes(5))

print(a.includes(b))
print(a.includes(Interval(3, 5)))
