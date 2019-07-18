def attr(x):
	return lambda t: (t[0] == x)

def is_number(x):
	try:
		float(x)
		return True
	except:
		return False

def true(x):
	return True

def false(x):
	return False

def match(a1, a2):

	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])

		return left == right

	return _inner 


