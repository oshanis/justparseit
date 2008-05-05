"""
6.863 Spring 2008 Project

The RDF Generator
"""
import sys
import logging

# Configure how we want rdflib logger to log messages
_logger = logging.getLogger("rdflib")
_logger.setLevel(logging.DEBUG)
_hdlr = logging.StreamHandler()
_hdlr.setFormatter(logging.Formatter('%(name)s %(levelname)s: %(message)s'))
_logger.addHandler(_hdlr)

from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF

#from pparser import *
#from Condition import *

def doCommand():
	"""Command line NLP AIR Policy Generator

        --help        print this message
        --entity "ENTITY NAME"    
        <command> <options> <steps> [--with <more args> ]
	"""

def parseNL():
	""""Eunsuk's Dictionary"""
	#{'ENTITY': 'MIT', 'ACTION': 'use', 'Flag': True, 'PURPOSE': 'criminal', 'Policy': 'MIT prox card policy', 'DATA': 'proxy', 'Condition': <Condition.AndCond instance at 0x1e81120>}

	POLICY_TXT = "MIT Proximity Card Data Policy"
	ENTITY_TXT =" Committee on Discipline (CoD)"
	ACTION_TXT = "use"
	DATA_TXT = "proximity card data"
	PURPOSE_TXT = "criminal investigation"
	CONDITION_VAL = None
	FLAG_VAL = True
	components = {'ENTITY': ENTITY_TXT, 'ACTION': ACTION_TXT, 'Flag': FLAG_VAL, 'DATA':DATA_TXT, 'PURPOSE':PURPOSE_TXT, 'POLICY':POLICY_TXT, 'Condition': CONDITION_VAL }
	
	#components = run()
	return components
   
def fragIDs(components):
	for x in components:
		if type(x) != bool:
			print x
			components[x] = "#" + components[x].replace(" ","_") 
	return components


def getMatch(term):

	"""
		This is a method for extracting the exact RDF term class for the string fragment from the Sentence parser
	"""
	g = Graph()
	g.load("data/university.n3", format="n3")
	matches = []
	for row in g.query('select ?a WHERE { ?a rdfs:label "'+ term +'"}',initNs=dict(rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"))):
		matches.append(row[0])
	return matches[0] #TODO: what is there are more than 1 match?
    
    
def constructPolicy():
	
	store = Graph()
	
	dict = parseNL()
	frags = fragIDs(dict)
	
	# Bind a few prefix, namespace pairs.
	store.bind("air", "http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	store.bind("pur", "http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	store.bind("owl", "http://www.w3.org/2002/07/owl#")

	# Create namespace objects
	AIR = Namespace("http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	PUR = Namespace("http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	OWL = Namespace("http://www.w3.org/2002/07/owl#")
	
	"""This should come from the user"""
	store.bind("mit", "http://dig.csail.mit.edu/TAMI/2007/s0/university#")
	MIT = Namespace("http://dig.csail.mit.edu/TAMI/2007/s0/university#")
	
	# create the policy
	policy = URIRef(frags['POLICY'])
	
	store.add((policy, RDF.type, AIR["Policy"]))
	store.add((policy, AIR["label"], Literal(dict['POLICY'])))
	# add the variables
	store.add((policy, AIR["variable"], URIRef("#U")))
	store.add((policy, AIR["variable"], URIRef("#D")))
	store.add((policy, AIR["variable"], URIRef("#P")))
	conditionCount = 1
	
	rule = "rule_"+conditionCount.__str__()
	rule = URIRef(rule)
	store.add((policy, AIR["rule"], rule))
	
	"""
		Construct the pattern for the data
	"""
	store.add((rule, RDF.type, AIR["BeliefRule"]))
	pattern_1 = Graph()
	store.add((rule, AIR["pattern"], pattern_1))
	pattern_1.add((URIRef("#U"), RDF.type, AIR["UseEvent"]))
	pattern_1.add((URIRef("#U"), AIR["data"], URIRef("#D")))
	pattern_1.add((URIRef("#U"), AIR["purpose"], URIRef("#P")))


	"""
		@todo: Get the condition count from Eunsuk
		totalConditions = Condition.count()
	"""
	totalConditions = 1
	
	while (conditionCount < totalConditions):
		"""Handle the conditions here """
		conditionCount = conditionCount + 1
		rule = "rule_"+conditionCount.__str__()
		rule = URIRef(rule)
	

	# create the rule body

	# Serialize and save the result
	store.serialize("policy.n3", format="n3")

	# Serialize as N3
	print store.serialize(format="n3")

	

if __name__ == '__main__':
    constructPolicy()
