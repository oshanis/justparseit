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
from rdflib.syntax.parsers.N3Parser import N3Parser

def doCommand():
	"""Command line NLP AIR Policy Generator

        --help        print this message
        --entity "ENTITY NAME"    
        <command> <options> <steps> [--with <more args> ]
	"""

def parseNL():
    
    POLICY_TXT = "MIT Proximity Card Data Policy"
    ENTITY_TXT =" Committee on Discipline (CoD)"
    ACTION_TXT = "use"
    DATA_TXT = "proximity card data from the card reader logs"
    PURPOSE_TXT = "criminal investigation"
    CONDITION_TXT = "NULL"
    FLAG = "true"
    components = {'POLICY':POLICY_TXT, 'ENTITY': ENTITY_TXT, 'ACTION': ACTION_TXT, 'DATA':DATA_TXT, 'PURPOSE':PURPOSE_TXT}
    return components
    
def fragIDs(components):
    new_components = {}
    for x in components:
        new_components[x] = "#" + components[x].replace(" ","_") 
    return new_components


def getMatch(term):

	"""
		This is a method for extracting the exact RDF term class for the string fragment from the Sentence parser
	"""
		
	print term
	g = Graph()
	g.load("data/university.n3", format="n3")
	matches = []
	for row in g.query('select ?a WHERE { ?a rdfs:label "'+ term +'"}',initNs=dict(rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"))):
		matches.append(row)
	return matches[0] #TODO: what is there are more than 1 match?
    
def constructPolicy():
	store = Graph()
	# Bind a few prefix, namespace pairs.
	store.bind("air", "http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	store.bind("pur", "http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	store.bind("mit", "http://dig.csail.mit.edu/TAMI/2007/s0/university#")
	store.bind("owl", "http://www.w3.org/2002/07/owl#")

	# Create namespace objects.
	AIR = Namespace("http://dig.csail.mit.edu/TAMI/2007/amord/air#")
	PUR = Namespace("http://dig.csail.mit.edu/TAMI/2006/s4/purposes#")
	MIT = Namespace("http://dig.csail.mit.edu/TAMI/2007/s0/university#")
	OWL = Namespace("http://www.w3.org/2002/07/owl#")
	
	f = fragIDs(parseNL())
	# create the policy
	policy = URIRef(f['POLICY'])
	store.add((policy, RDF.type, AIR["Policy"]))

	# add the variables
	store.add((policy, AIR["variable"], URIRef("#U")))
	store.add((policy, AIR["variable"], URIRef("#D")))
	store.add((policy, AIR["variable"], URIRef("#P")))

	# add the outer rule
	outer_rule = BNode()
	store.add((policy, AIR["rule"], outer_rule))
	
	outer_rule_pattern = Graph()
	outer_rule_pattern.add((URIRef("#U"), RDF.type, AIR["UseEvent"]))
	outer_rule_pattern.add((URIRef("#U"), AIR["data"], URIRef("#D")))
	outer_rule_pattern.add((URIRef("#U"), AIR["purpose"], URIRef("#P")))
	outer_rule_pattern.add((URIRef("#D"), RDF.type, MIT["ProxCardEvent"]))

	store.add((policy, AIR["pattern"], outer_rule_pattern))

	# create the rule body
	store.add((outer_rule, AIR["label"], Literal("MIT prox-card policy")))
	store.add((outer_rule, AIR["pattern"], Literal("MIT prox-card policy")))

	# Serialize and save the result
	store.serialize("policy.n3", format="n3")

	# Serialize as N3
	print store.serialize(format="n3")

	a = "proximity card data"
	print getMatch(a)

if __name__ == '__main__':
    constructPolicy()
