import random

class MatrixException(Exception):
  """
  Class storing matrix exception raised when dimensions or values mismatch.
  """
  
  def __init__(self, string):
    super().__init__("MatrixException: " + string)

class VectorException(Exception):
  """
  Class storing vector exception raised when dimensions or values mismatch.
  """
  
  def __init__(self, string):
    super().__init__("VectorException: " + string)

class UnsupportedException(Exception):
  """
  Class storing exception raised when unsupported function is called.
  """
  
  def __init__(self):
    super().__init__("Exception: unsupported operation for this class")

class Matrix:
  """
  Class storing real n x m matrix represented by list of lists.
  Matrix is initialized with random elements from interval [0, 1).
  """
  
  def __init__(self, n, m):
    if not isinstance(n, int) or type(m) is not int or n <= 0 or m <= 0:
      raise MatrixException("matrix dimensions must be positive integers")
      
    self.A = [[random.random() for _ in range(m)] for _ in range(n)]
  
  def __repr__(self):
    return self.__class__.__name__ + "(" + str(self.get_n()) + ", " + str(self.get_m()) + ", " + str(self.A) + ")"
  
  def __str__(self):
    return "\n".join(["| " + " ".join(["{:5.2f}".format(self.A[i][j]) for j in range(self.get_m())]) + " |" for i in range(self.get_n())]) + "\n"
  
  def get_n(self):
    return len(self.A)

  def get_m(self):
    return len(self.A[0])

  def get_dims(self):
    return (self.get_n(), self.get_m())

  def get_norm(self):
    return sum([self.A[i][j] * self.A[i][j] for i in range(self.get_n()) for j in range(self.get_m())])**0.5
  
  def __getitem__(self, i):
    if not isinstance(i, int) or i < 0 or i >= self.get_n():
      raise MatrixException("index is not integer or out of matrix range")
      
    return self.A[i]
  
  def __setitem__(self, i, vector):
    if not isinstance(i, int) or i < 0 or i >= self.get_n():
      raise MatrixException("index is not integer or out of matrix range")
    elif not isinstance(vector, list) and not isinstance(vector, Vector):
      raise MatrixException("matrix row must be vector or list of numbers")
    elif len(vector) != self.get_m():
      raise MatrixException("matrix and vector dimensions mismatch")
      
    self.A[i] = vector if isinstance(vector, list) else [vector[i] for i in range(len(vector))]
    
  def add(self, matrix):
    if not isinstance(matrix, Matrix):
      raise MatrixException("argument must be matrix")
    elif self.get_dims() != matrix.get_dims():
      raise MatrixException("matrices' dimensions mismatch")
      
    for i in range(self.get_n()):
      for j in range(self.get_m()):
        self[i][j] += matrix[i][j]

  def multiply(self, matrix):
    if not isinstance(matrix, Matrix):
      raise MatrixException("argument must be matrix")
    elif self.get_m() != matrix.get_n():
      raise MatrixException("matrices' dimensions mismatch")
      
    self.A = (self * matrix).A

  def __add__(self, matrix):
    if not isinstance(matrix, Matrix):
      raise MatrixException("argument must be matrix")
    elif self.get_dims() != matrix.get_dims():
      raise MatrixException("matrices' dimensions mismatch")
      
    M = Matrix(self.get_n(), self.get_m())
    for i in range(M.get_n()):
      for j in range(M.get_m()):
        M[i][j] = self[i][j] + matrix[i][j]
        
    return M
  
  def __mul__(self, matrix):
    if not isinstance(matrix, Matrix):
      raise MatrixException("argument must be matrix")
    elif self.get_m() != matrix.get_n():
      raise MatrixException("matrices' dimensions mismatch")
      
    M = Matrix(self.get_n(), matrix.get_m())
    for i in range(M.get_n()):
      for j in range(M.get_m()):
        M[i][j] = sum([self[i][k] + matrix[k][j] for k in range(self.get_m())])
        
    return M

  def __call__(self, vector):
    if not isinstance(vector, list) and not isinstance(vector, Vector):
      raise MatrixException("argument must be vector or list of numbers")
    elif len(vector) != self.get_m():
      raise MatrixException("matrix and vector dimensions mismatch")
      
    product = Vector(self.get_n())
    for i in range(self.get_n()):
      product[i] = sum([self.A[i][j] * vector[j] for j in range(self.get_m())])
      
    return product

class Square(Matrix):
  """
  Class storing real n x n square matrix represented by list of lists.
  Matrix is initialized with random elements from interval [0, 1).
  """
  
  def __init__(self, n):
    super().__init__(n, n)
  
  def __repr__(self):
    return self.__class__.__name__ + "(" + str(self.get_n()) + ", " + str(self.A) + ")"

  def get_trace(self):
    return sum([self.A[i][i] for i in range(self.get_n())])

class Triangular(Square):
  """
  Class storing real n x n upper triangular matrix represented by list of lists.
  Matrix is initialized with random elements from interval [0, 1).
  """
  
  def __init__(self, n):
    super().__init__(n)
    self.A = [[random.random() if i <= j else 0 for j in range(n)] for i in range(n)]

  def __setitem__(self, i, vector):
    raise UnsupportedException()

class Identity(Square):
  """
  Class storing n x n identity matrix represented by list of lists.
  Matrix is initialized with elements from set {0, 1}.
  """
  def __init__(self, n):
    super().__init__(n)
    self.A = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

  def __setitem__(self, i, vector):
    raise UnsupportedException()

class Vector(Matrix):
  """
  Class storing real vector of size n represented by list of lists.
  Vector is initialized with random elements from interval [0, 1).
  """
  
  def __init__(self, n):
    if not isinstance(n, int) or n <= 0:
      raise VectorException("vector dimension must be positive integer")
      
    super().__init__(n, 1)

  def __repr__(self):
    return self.__class__.__name__ + "(" + str(self.get_n()) + ", " + str([self.A[i][0] for i in range(self.get_n())]) + ")"

  def __len__(self):
    return self.get_n()
    
  def __getitem__(self, i):
    if not isinstance(i, int) or i < 0 or i >= self.get_n():
      raise VectorException("index is not integer or out of vector range")
      
    return self.A[i][0]

  def __setitem__(self, i, value):
    if not isinstance(i, int) or i < 0 or i >= self.get_n():
      raise VectorException("index is not integer or out of vector range")
    elif not isinstance(value, int) and not isinstance(value, float):
      raise VectorException("vector value must be integer or real number")
      
    self.A[i][0] = value

  def normalize(self):
    norm = self.get_norm()
    
    for i in range(self.get_n()):
      self[i] /= norm
    
  def add(self, vector):
    if not isinstance(vector, list) and not isinstance(vector, Vector):
      raise VectorException("argument must be vector or list of numbers")
    elif len(self) != len(vector):
      raise VectorException("vectors' dimensions mismatch")
      
    for i in range(self.get_n()):
      self[i] += vector[i]

  def multiply(self, vector):
    if not isinstance(vector, list) and not isinstance(vector, Vector):
      raise VectorException("argument must be vector or list of numbers")
    elif len(self) != len(vector):
      raise VectorException("vectors' dimensions mismatch")
      
    for i in range(self.get_n()):
      self[i] *= vector[i]
      
  def __add__(self, vector):
    if not isinstance(vector, list) and not isinstance(vector, Vector):
      raise VectorException("argument must be vector or list of numbers")
    elif len(self) != len(vector):
      raise VectorException("vectors' dimensions mismatch")
      
    V = Vector(self.get_n())
    for i in range(V.get_n()):
      V[i] = self[i] + vector[i]
      
    return V
  
  def __mul__(self, vector):
    if not isinstance(vector, list) and not isinstance(vector, Vector):
      raise VectorException("argument must be vector or list of numbers")
    elif len(self) != len(vector):
      raise VectorException("vectors' dimensions mismatch")
      
    return Vector.dot_product(self, vector)

  @staticmethod
  def dot_product(first, second):
    if not isinstance(first, list) and not isinstance(first, Vector) or not isinstance(second, list) and not isinstance(second, Vector):
      raise VectorException("arguments must be vectors or lists of numbers")
    elif len(first) != len(second):
      raise VectorException("vectors' dimensions mismatch")
      
    return sum([first[i] * second[i] for i in range(len(first))])

class Indicator(Vector):
  """
  Class storing indicator vector of size n represented by list of lists.
  Vector is initialized with elements from set {0, 1}.
  """
  
  def __init__(self, n, i = 0):
    if not isinstance(n, int) or n <= 0:
      raise VectorException("vector dimension must be positive integer")
    elif not isinstance(i, int) or i < 0 or i >= n:
      raise VectorException("index is not integer or out of vector range")
      
    self.A = [[1 if i == j else 0] for j in range(n)]

  def __setitem__(self, i, value):
    raise UnsupportedException()

print('# creates real matrix A represented by class Matrix')

A = Matrix(5, 4)

print('# prints out type and representations of real matrix A')

print(type(A))
print(repr(A))
print(str(A))

print('# prints out standard properties of real matrix A')

print(A.get_n())
print(A.get_m())
print(A.get_dims())
print(A.get_norm())
try:
  print(A.get_trace())
except Exception as e:
  print(e)

print('# tests real matrix A getter and setter functions')

print(A[0])
print(A[0][1])

try:
  A[0] = [0, 1, 2, 3, random.random()]
except MatrixException as e:
  print(e)

A[0] = [0, 1, 2, random.random()]
print(A[0])
A[0][1] = random.random()
print(A[0])

print('# tests matrix A addition operator and function')

B = Matrix(A.get_n(), A.get_m())
print(B)

print(A + B)

A.add(B)
print(A)

print('# tests matrix A multiplication operator and function')

B = Matrix(A.get_m(), 5)
print(B)

print(A * B)

A.multiply(B)
print(A)

print('# creates real square matrix S represented by class Square')

S = Square(4)

print('# prints out type and representations of square matrix S')

print(type(S))
print(repr(S))
print(str(S))

print('# prints out standard properties of square matrix S')

print(S.get_n())
print(S.get_dims())
print(S.get_norm())
print(S.get_trace())

print('# creates real triangular matrix T represented by class Triangular')

T = Triangular(3)

print('# prints out type and representations of triangular matrix T')

print(type(T))
print(repr(T))
print(str(T))

print('# prints out standard properties of triangular matrix T')

print(T.get_n())
print(T.get_dims())
print(T.get_norm())
print(T.get_trace())

print('# creates identity matrix I represented by class Identity')

I = Identity(4)

print('# prints out type and representations of identity matrix I')

print(type(I))
print(repr(I))
print(str(I))

print('# prints out standard properties of identity matrix I')

print(I.get_n())
print(I.get_dims())
print(I.get_norm())
print(I.get_trace())

print('# tests identity matrix I getter and setter functions')

print(I[0])
print(I[0][1])

try:
  I[0] = [0, 1, random.random()]
except Exception as e:
  print(e)

print('# creates real vector x represented by class Vector')

x = Vector(A.get_m())

print('# prints out type and representations of real vector x')

print(type(x))
print(repr(x))
print(str(x))

print('# prints out standard properties of real vector x')

print(len(x))
print(x.get_n())
print(x.get_dims())
print(x.get_norm())
x.normalize()
print(x.get_norm())

print('# tests real vector x getter and setter functions')

print(x[0])
x[0] = random.random()
print(x[0])

print('# tests vector x addition operator and function')

y = Vector(x.get_n())
print(y)

print(x + y)

x.add(y)
print(x)

print('# tests vector x multiplication operator and function')

print(x * y)
print(Vector.dot_product(x, y))

x.multiply(y)
print(x)

print('# creates indicator vector i represented by class Indicator')

i = Indicator(x.get_n(), x.get_n() // 2)

print('# prints out type and representations of indicator vector i')

print(type(i))
print(repr(i))
print(str(i))

print('# prints out standard properties of indicator vector i')

print(len(i))
print(i.get_n())
print(i.get_dims())
print(i.get_norm())

print('# tests matrix A multiplication by vector operator')

print(A(x))

print(A(y))
