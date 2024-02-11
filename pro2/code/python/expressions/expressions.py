
def generate(expr, nums, ops):
  if not nums:
    return [expr]
  exprs = generate(expr + nums[0], nums[1:], ops)
  for op in ops:
    exprs.extend(generate(expr + op + nums[0], nums[1:], ops))
  return exprs

def evaluate(exprs, val):
  return [expr for expr in exprs if eval(expr) == val]

NUMS = '123456789'
OPS = '+-*/'
VAL = 2024

# generates all arithmetic expressions with NUMS and OPS

exprs = generate(NUMS[0], NUMS[1:], OPS)

# finds arithmetic expressions that evaluate to VAL

exprs = evaluate(exprs, VAL)

# prints out valid arithmetic expressions

for expr in exprs:
  print(VAL, "=", expr)
