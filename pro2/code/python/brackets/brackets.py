
BRACKETS = {')': '(', ']': '[', '}': '{'}

def is_valid(str):
  stack = []
  for char in str:
    if char in BRACKETS.values():
      stack.append(char)
    elif char in BRACKETS:
      if not stack or stack.pop() != BRACKETS[char]:
        return False
  return not stack

for brackets in ["([{a}])", "([a]{b})", "{a}[ ](b)", "([a)", "([a)]", "({}[])()", "({a][b)c}"]:
  print(brackets + ": " + str(is_valid(brackets)))
