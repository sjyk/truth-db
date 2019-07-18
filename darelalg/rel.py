class DARelation(object):

	def __init__(self, data):
		self.data = [set(rec) for rec in data]

	def __or__(self, cond):
		return DARelation([rec for rec in self.data if cond(rec)])

	def __getitem__(self, key):

		try:
		    iter(key)
		    helper = lambda a: any([k(a) for k in key])
		except TypeError as te:
		    helper = lambda a: key(a)
		
		return DARelation([set([attr for attr in rec if helper(attr)]) for rec in self.data])


	def map(self, fn):
		return DARelation([set([fn(attr) for attr in rec]) for rec in self.data])


	def __mul__(self, other):
		return DARelation([i.union(j) for i in other.data for j in self.data])

	def __add__(self, other):
		return DARelation(self.data + other.data)

	def __str__(self):
		return str(self.data)

	__repr__ = __str__


