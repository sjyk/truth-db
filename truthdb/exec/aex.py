# -*- coding: utf-8 -*-
"""This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This file describes the language primitives for attribute expressions.
"""
import re


"""Label manipulation primitives

A labeled attribute is one of the form ('Label', value)
"""

def is_labeled(x):
	"""Returns all attributes that are labeled

	Example: rel = [{('a',1), 'b', 3}, {('a',2), 'f', 'g'}]
	
	>>rel[is_labeled]
	[{('a',1)}, {('a',2)}]

	"""
	try:
		iter(x)
		return (len(x) == 2)
	except:
		return False


def label(x, regex=False):
	"""Extracts all labels, accepts regexes

	Example: rel = [{('a',1), 'b', 3}, {('a',2), 'f', 'g'}]
	
	>>rel[label('a')]
	[{('a',1)}, {('a',2)}]

	"""

	def _inner(t):
		try:
			if regex:
				return bool(re.seach(x,t[0]))
			else:
				return (x == t[0])
		except:
			return False

	return _inner


"""Used in map functions to label data.
"""
def label_if(label, cond):
	def _inner(t):
		if cond(t):
			return (label, t)
		else:
			return t
	return _inner


"""Number manipulation primitives
"""

def is_number(x):
	"""Extracts all values that are numerical

	Example: rel = [{('a',1), 'b', 3}, {('a',2), 'f', 'g'}]
	
	>>rel[is_number]
	[{3}]

	"""
	try:
		float(x)
		return True
	except:
		return False


def is_number_value(x):
	"""Extracts all values that are numerical (even if labeled)

	Example: rel = [{('a',1), 'b', 3}, {('a',2), 'f', 'g'}]
	
	>>rel[is_number]
	[{3}]
	"""
	if is_labeled(x):
		try:
			float(x[1])
			return True
		except:
			return False
	else:
		return is_number(x)