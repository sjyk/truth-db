# -*- coding: utf-8 -*-
"""This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This module implements the intermediate relational representation for 
TruthDB. Our objective is to unify query processing over structured and 
unstructured data. To do so, we define a `dynamically-attributed` tuple.

Every Dynamically-Attributed tuple is a set of atomic data, e.g.,
{‘a’, ‘7’, ‘q’, ‘2019’}

This set constitutes one tuple. A Dynamically-Attributed relation is a 
multiset of such DA tuples:
{	
	{‘a’, ‘7’, ‘q’, ‘2019’},
	{‘a’, ‘7’, ‘q’, ‘2019’, 4}
}

We can define select, project, join, and aggregate operations over these
tuples akin to the definitions for standard relational algebra. 

A tuple expression (tex) is Boolean function that maps from tuples to true, false. 
Example: lambda tup: 'a' in tup

An attribute expression (aex) is a boolean condition that maps dom->{true, false}. 
Example: isNumber(value)

So, then the basic algebra is:
select(tex) #find all tuples that satisfy tex
project(aex) #filter each tuple by only those values that satisfy aex
groupby(aex) #group each tuple by those distinct values that satisfy aex
union()
difference()
cart() 
join(tex) 
"""

class DARelation(object):
	"""DARelation: This class defines the main dynamically-attributed relation.

	All operations on DARelation objects operate functionally making copies. Each
	tuple is a python type(set). 

	Tuple Expressions are functions that take in a set and output a boolean
	Attribute Expressions are functions that take in a value and output a boolean
	"""


	def __init__(self, data):
		"""DARelation constructor takes input data in the form of a collection
		   of tuples.

	    Args:
	        data (Iterable[Iterable]): The input data.
	    """

		self.data = [set(rec) for rec in data]


	def __or__(self, tex):
		"""select operator

		select works similar to the relational algebra select operator. It
		takes a set of tuples as input and returns a set of tuples that 
		satisfy tex. We overload the | operator for syntactic reasons.

		Args:
	        tex (lambda tuple: boolean, tuple expression): A tuple expression

	    Example:
	    	(rel | lambda tup: 'a' in tup) 
	    	# returns all tuples that have an 'a' value.
	    """
		return DARelation([rec \
						  for rec in self.data 
						  if tex(rec)])

	def __getitem__(self, aex):
		"""project operator

		project is a generalization of the project operator seen in standard
		relational algebra. Given a set of attribute expressions project 
		restricts the set of attributes to those that satisfy the attribute
		expression.

		Args:
	        aex (lambda value: boolean, value expression): A value expression

	    Example:
	    	rel[is_number]
	    	#projects all tuples onto those attributes that are numerical
	    """

		if is_iterable(aex)
		    helper = lambda a: any([k(a) for k in aex])
		else:
		    helper = lambda a: aex(a)
		


		marker = None
		try:
			data = []
			for rec in self.data:
				marker = rec
				data.append(set([attr for attr in rec if helper(attr)]))
			return DARelation(data)
		except:
			raise TupleTypeException("Error occurred at: " + str(marker))



	def __mul__(self, other):
		"""cartesian operator

		cartesian operator takes all pairs of tuples from two DArelations
		and returns a new DARelation with the allpairs union.

		Args:
	        aex (lambda value: boolean, value expression): A value expression

	    Example:
	    	rel1*rel2

		"""
		return DARelation([i.union(j) for i in other.data for j in self.data])
	

	def group_by(self, key):
		"""group by operator

		The group by operator generates a new grouped relation. It groups
		elements by the distinct values of the attribute expression. This 
		function is implemented as a hash aggregation.

		Args:
	        key (lambda value: boolean, value expression): A value expression

	    Example:
	    	rel1.group_by(is_number)

		"""

		state = {}
		for tup in self.data:
			relevant_attrs = tuple([rec for rec in tup if key(rec)])

			if len(relevant_attrs) == 0:
				pass
			
			if relevant_attrs not in state:
				state[relevant_attrs] = []

			state[relevant_attrs].extend(tup)

		return DARelation([list(k) + list(state[k]) for k in state])




	def map(self, fn):
		"""map operator

		Applies a function to each value in the tuple

		Args:
	        fn (lambda value: value): A mapping function

	    Example:
	    	rel1.map(str)

		"""
		return DARelation([set([fn(attr) for attr in rec]) for rec in self.data])

	def enumerate(self):
		"""enumerate operator

		Adds an id number to each tuple

	    Example:
	    	rel1.enumerate()

		"""
		return DARelation([rec.union(set([('id', i)])) for i,rec in enumerate(self.data)])

	def __str__(self):
		return str(self.data)

	__repr__ = __str__



def is_iterable(dat):
	"""is_iterable tests to see if an object is iterable

		Args:
	        daata (object): an object
	"""

	try:
		iter(data)
		return True
	except TypeError as te:
		return False



class TupleTypeException(Exception):
	"""This is an uninteresting placeholder that defines a 
	custom exception for now
	"""
	pass



