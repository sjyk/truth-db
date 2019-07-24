# -*- coding: utf-8 -*-
"""This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This file describes the language primitives for tuple expressions.
"""


"""Basic filter conditions
"""
def exists(x):
	return lambda t: x in t

def existsAttribute(x):

	def _inner(tup):
		for t in tup:
			try:
				if t[0] == x:
					return True
			except:
				pass
		return False

	return _inner

def existsValue(x):

	def _inner(tup):
		for t in tup:
			try:
				if t[1] == x:
					return True
			except:
				pass
		return False

	return _inner



"""Join conditions (assumes cart is materialized)
"""

def match(a1, a2):
	"""Exact equality on two attribute conditions
	"""
	return jaccard(a1,a2, 1.0)


def jaccard(a1, a2, thresh):
	"""Match on jaccard similarity
	"""

	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])
		jac = len(left.intersection(right))/len(left.union(right))

		return (jac >= thresh)

	return _inner 

def atl_one(a1, a2):
	"""If at least one hit
	"""

	def _inner(tup):
		left = set([a[1] for a in tup if a1(a)])
		right = set([a[1] for a in tup if a2(a)])

		return (len(left.intersection(right)) > 0)

	return _inner