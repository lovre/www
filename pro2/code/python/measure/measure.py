
class Measurement:

  def __init__(self, val, err = 0.0):
    if err < 0.0:
      raise Exception('negative measurement error')
  
    self.val = val
    self.err = err
    self.rel = abs(err / val)
    
  def __repr__(self):
    return "Measurement(" + str(self.val) + ", " + str(self.err) + ")"
    
  def __str__(self):
    return str(self.val) + (" ± " + str(self.err) if self.err > 0.0 else "")
    
  def __add__(self, m):
    return Measurement(self.val + m.val, self.err + m.err)
    
  def __sub__(self, m):
    return Measurement(self.val - m.val, self.err + m.err)
  
  def __mul__(self, m):
    return Measurement(self.val * m.val, (self.rel + m.rel) * abs(self.val * m.val))

a = Measurement(1.5)
b = Measurement(0.5, 0.01)
c = Measurement(-1.5, 0.1)

print("a =", a)
print("c =", c)
print("a+b =", a + b)
print("a-b+c =", a - b + c)
print("a*b*c =", a * b * c)
print("a*(b+c) =", a * (b + c))
