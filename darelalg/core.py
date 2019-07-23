def attr(x):
	def _inner(t):
		try:
			return t[0] == x
		except:
			return false

	return _inner


def suffix(x):
	return lambda t: (x in t[0])


def label_if(label, cond):
	def _inner(t):
		if cond(t):
			return (label, t)
		else:
			return t
	return _inner


def is_number(x):
	try:
		float(x)
		return True
	except:
		return False


def number_attributes(x):
	try:
		float(x[1])
		return True
	except:
		return False


def true(x):
	return True

def false(x):
	return False

def match(a1, a2):
	return jaccard(a1,a2, 1.0)

def exists(x):
	return lambda t: x in t


def conj(a,b):
	return lambda t: a(t) and b(t)

def disj(a,b):
	return lambda t: a(t) or b(t)

def jaccard(a1, a2, thresh):
	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])
		jac = len(left.intersection(right))/len(left.union(right))
		
		return (jac >= thresh)

	return _inner 

def atl_one(a1, a2):
	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])

		return (len(left.intersection(right)) > 0)

	return _inner