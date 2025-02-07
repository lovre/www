
class Series:
  def __init__(self, a_n = lambda n: n):
    self.a_n = a_n # n-ti člen zaporedja a(n)
    
  def s_n(self, n = 1): # vsota prvih n členov s(n)
    return sum(self.a_n(i) for i in range(1, n + 1))
    
  def __repr__(self):
    return self.__class__.__name__ + "()"
    
class Arithmetic(Series):
  def __init__(self, d = 0.001):
    super().__init__(lambda n: d * n)
    self.d = d
    
  def __repr__(self):
    return super().__repr__()[:-1] + str(self.d) + ")"
    
class Geometric(Series):
  def __init__(self, r = 0.9):
    super().__init__(lambda n: r**n)
    self.r = r
    
  def __repr__(self):
    return super().__repr__()[:-1] + str(self.r) + ")"
    
class Harmonic(Series):
  def __init__(self):
    super().__init__(lambda n: 1 / n)

for series in [Arithmetic(), Geometric(), Harmonic()]:
  print(series)
  for n in [1, 10, 100, 1000]:
    print("a({}) = {:.3f}\ts({}) = {:.3f}".format(n, series.a_n(n), n, series.s_n(n)))
  print()
