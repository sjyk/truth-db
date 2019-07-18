def attr(x):
	return lambda t: (t[0] == x)

def suffix(x):
	return lambda t: (x in t[0])

def label(x, label):
	return lambda t: (label, t)

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

	return jaccard(a1,a2, 1.0)


def jaccard(a1, a2, thresh):

	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])
		jac = len(left.intersection(right))/len(left.union(right))

		return (jac >= thresh)

	return _inner 

