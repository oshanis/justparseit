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

sys.path.append("../PolicyParser/")
sys.path.append("../featureparse")


from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF


def doCommand():
	"""Command line NLP AIR Policy Generator

        --help        print this message
        --entity "ENTITY NAME"    
        <command> <options> <steps> [--with <more args> ]
	"""

def parseNL(name, sentence):
	""""Eunsuk's Dictionary"""
	#{'ENTITY': 'MIT', 'ACTION': 'use', 'Flag': True, 'PURPOSE': 'criminal', 'Policy': 'MIT prox card policy', 'DATA': 'proxy', 'Condition': <Condition.AndCond instance at 0x1e81120>}

	POLICY_TXT = "MIT Proximity Card Data Policy"
	ENTITY_TXT =" Committee on Discipline (CoD)"
	ACTION_TXT = "use"
	DATA_TXT = "proximity card data"
	PURPOSE_TXT = "criminal investigation"
	CONDITION_VAL = None
	FLAG_VAL = True
	#components = {'ENTITY': ENTITY_TXT, 'ACTION': ACTION_TXT, 'FLAG': FLAG_VAL, 'DATA':DATA_TXT, 'PURPOSE':PURPOSE_TXT, 'POLICY':POLICY_TXT, 'CONDITION': CONDITION_VAL }
	
	from pparser import parsePolicy
	components = parsePolicy(name, sentence)
	return components
   
def getMatch(term, domain):

	print domain
	"""
		This is a method for extracting the exact RDF term class for the string fragment from the Sentence parser
	"""
	g = Graph()
	g.load(domain, format="n3")
	matches = []
	for row in g.query('select ?a WHERE { ?a rdfs:label "'+ term +'"}',initNs=dict(rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"))):
		matches.append(row[0])
	if len(matches)>0:	
		return matches[0] #TODO: what is there are more than 1 match?
	else:
		return None
    
    
def constructPolicy(dict, domain):
	
	store = Graph()
	
	# Bind a few prefix, namespace pairs.
	store.bind("air", "http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	store.bind("pur", "http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	store.bind("owl", "http://www.w3.org/2002/07/owl#")

	# Create namespace objects
	AIR = Namespace("http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	PUR = Namespace("http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	OWL = Namespace("http://www.w3.org/2002/07/owl#")
	
	"""This should come from the user"""
	#domain = "http://dig.csail.mit.edu/TAMI/2007/s0/university#"
	store.bind("mit", domain)
	MIT = Namespace(domain)
	
	# create the policy
	p = "#" + dict['POLICY'].replace(" ","_") 
	policy = URIRef(p)
	
	store.add((policy, RDF.type, AIR["Policy"]))
	store.add((policy, AIR["label"], Literal(dict['POLICY'])))
	# add the variables
	store.add((policy, AIR["variable"], URIRef("#U")))
	store.add((policy, AIR["variable"], URIRef("#A")))
	store.add((policy, AIR["variable"], URIRef("#D")))
	store.add((policy, AIR["variable"], URIRef("#P")))
	conditionCount = 0
	
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
	pattern_1.add((URIRef("#U"), AIR["actor"], URIRef("#A")))
	pattern_1.add((URIRef("#U"), AIR["data"], URIRef("#D")))
	pattern_1.add((URIRef("#U"), AIR["purpose"], URIRef("#P")))

	assertion = Graph()
	store.add((rule, AIR["assert"], assertion))
	if dict['FLAG']:
	   assertion.add((URIRef("#U"), AIR["compliant-with"], policy))
	else:
		assertion.add((URIRef("#U"), AIR["non-compliant-with"], policy))
	
	totalConditions = len(dict['CONDITION'])
	print totalConditions
	conditions = dict['CONDITION']
	# create the rule body
	while (conditionCount < totalConditions):
		"""Handle the conditions here """
		conditionCount = conditionCount + 1
		mathced_cond = getMatch(conditions[conditionCount], domain)
		if mathced_cond != None:
			"""The term should exist in the ontology"""
			new_rule = "rule_"+conditionCount.__str__()
			new_rule = URIRef(rule)
			store.add((rule, AIR["rule"], new_rule))
			pattern = Graph()
			store.add((new_rule, AIR["pattern"], pattern))
			#pattern.add((URIRef("#A"), AIR[""]))

		
	# Serialize as N3
	return store.serialize(format="n3")


def gen_main(name, sentence, domain):
	dict = parseNL(name, sentence)
	parsed = constructPolicy(dict,domain)
	print parsed
	
	

if __name__ == '__main__':
	
	
	from pparser import parsePolicy
	from Condition import *

	name = "MITProxCardDataPolicy"
	sentence = "MIT can use proxy for criminal"
	domain = "../data/university.n3"
	
	gen_main(name, sentence, domain)
