# -*- coding: utf-8 -*-
"""This file is part of TruthDB which is released under MIT License and 
is copyrighted by the University of Chicago Database Group.

This file describes the core boolean manipulation primitives
"""
def true(x):
	return True

def false(x):
	return False

def conj(a,b):
	return lambda t: a(t) and b(t)

def disj(a,b):
	return lambda t: a(t) or b(t)

def implies(a,b):
	return lambda t: (not a(t)) or b(t)

def iff(a,b):
	return lambda t: conj(implies(a,b), implies(b,a))


