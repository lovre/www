print('Pozdravljeni pri predmetu PRO2!')

x = 1
y = 1.23
ch = 'a'
st = "niz znakov"

G = 9.81

if x < 1:
	print("Vrednost spremenljivke x je manjša od 1")
elif x < 2:
	print("Vrednost spremenljivke x je med 1 in 2")
else:
	print("Vrednost spremenljivke x je večja ali enaka 2")
 
for i in range(5):
	print("Vrednost spremenljivke i je enaka " + str(i))
 
i = 0
while i < 5:
	print("Vrednost spremenljivke i je enaka " + str(i))
	i += 1
 
def method(i):
	print("Vrednost parametra i je enaka " + str(i))
  
method(7)

def function(i):
	print("Vrednost parametra i je enaka " + str(i))
	i *= 7
	print("Vrednost rezultata funkcije je enaka " + str(i))
	return i

function(2)

inc = lambda x: x + 1

print(inc(0))

pow = lambda x, y: x**y

print(pow(2, 10))

def func(x):
  return lambda y: x * y
dbl = func(2)

print(dbl(10))
