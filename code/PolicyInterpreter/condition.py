"""
6.863 Spring 2008 Project

Definition for the Condition class

Each Cond object is a triple <subject, predicate, object>
"""

class Cond:
	def __init__(self, subject, predicate, object):
		self.subject = subject
		self.predicate = predicate
		self.object = object
#		print subject
#		print predicate
#		print object

	def getSubject(self):
		return self.subject
	
	def getPredicate(self):
		return self.predicate
	
	def getObject(self):
		return self.object
