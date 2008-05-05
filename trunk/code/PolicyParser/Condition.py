"""
6.863 Spring 2008 Project

Definition for the Condition class

Each Cond object is a boolean expression made out of
atomic Conds, AND, and OR
"""

class Cond:

	def isAnd(self):
		return False
	
	def isOr(self):
		return False
		
	def isAtomic(self): 
		return False
	
	def size(self):
		return 0
	
class AtomicCond(Cond):
	
	def __init__(self, atomicCond):
		self.atom = atomicCond
		
	def isAtomic(self):
		return True

	def getAtomicCond(self):
		 return self.atom
	
	def size(self):
		return 1
		
class CompositeCond(Cond):
	
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def getLeftCond(self):
		return self.left
	
	def getRightCond(self):
		return self.right
	
	def size(self):
		return self.left.size() + self.right.size()
	
class AndCond(CompositeCond):
	  
	def isAnd(self):
		return True
	
class OrCond(CompositeCond):
	  
	def isOr(self):
		return True

