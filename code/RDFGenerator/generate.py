"""
6.863 Spring 2008 Project

The RDF Generator
"""
import sys
import sys
import logging

sys.path.append("../PolicyInterpreter")
sys.path.append("../featureparse")
sys.path.append("../rdflib")
	
from policyParser import *

# Configure how we want rdflib logger to log messages
_logger = logging.getLogger("rdflib")
_logger.setLevel(logging.DEBUG)
_hdlr = logging.StreamHandler()
_hdlr.setFormatter(logging.Formatter('%(name)s %(levelname)s: %(message)s'))
_logger.addHandler(_hdlr)

from rdflib.Graph import Graph
from rdflib import URIRef, Literal, BNode, Namespace
from rdflib import RDF

def parseNL(name, sentence):
	"""This method will call the Policy Parser and get the relevant components
	components = {'ENTITY': ENTITY_TXT, 'ACTION': ACTION_TXT, 'FLAG': FLAG_VAL, 'DATA':DATA_TXT, 'PURPOSE':PURPOSE_TXT, 'POLICY':POLICY_TXT,
		 'CONDITION': CONDITION_VAL, 'PASSIVE_ENTITY': PASSIVE_ENTITY_VAL }
	"""
	components = parsePolicy(name, sentence)
	return components


def getVariable(dictVal):
	"""
	Just a convenient method for returning which variable corresponds to which
	"""
	#Python doesn't support switch?
	if dictVal == "ENTITY":
		return "#A"
	elif dictVal == "ACTION":
		return "#U" #Will make the assumption that all the actions are air:useEvent type
	elif dictVal == "DATA":
		return "#D"
	elif dictVal == "PURPOSE":
		return "#P"
	elif dictVal == "TRANSFEREE":
		return "#T"
	else:
		return None

	

def getMatch(term, domain):
	"""
		This is a method for extracting the exact RDF term class for the string fragment from the Sentence parser
	"""
	g = Graph()
	g.load(domain, format="n3")
	matches = []
	"""SPARQL query to match the correct subject"""
	for row in g.query('select ?a WHERE { ?a rdfs:label "'+ term +'"}',initNs=dict(rdfs=Namespace("http://www.w3.org/2000/01/rdf-schema#"))):
		matches.append(row[0])
	if len(matches)>0:	
		return matches[0] #TODO: what is there are more than 1 match?
	else:
		return None
	

def constructPolicy(dict, domain):
	"""
		Constructs the AIR policy
		The AIR policy is of the following form where all the AIR rules are dereferenced from the previous AIR rule 
		(this is NOT the most optimal way of expressing an AIR policy, but with the way we have to handle the 
		'conditions' this is the best way of doing it):
		
		@prefix : <#>.
		@prefix air: <http://dig.csail.mit.edu/TAMI/2007/amord/air#>.
		@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>.
		#Any other prefixes
		
		 :POLICY_NAME a air:Policy;
		     air:label "POLICY NAME";
		     air:variable :A,
		         :D,
		         :P,
		         :U. 
			air:rule <rule_0>;
		     
		 <rule_0> a air:BeliefRule;
		     air:pattern {
		     :U a air:UseEvent;
		             air:actor :A;
		             air:data :D;
		             air:purpose :P. 
		 };
		     air:rule <rule_1>. 
		
		 <rule_1> 
		 	air:pattern {
				...
				...
		 };
		 air:assert {
		     :U air:compliant-with :POLICY_NAME. 
		 };

	"""
	
	if dict == None:
		return None
	else:
		
		store = Graph()
		
		# Bind a few prefix, namespace pairs.
		store.bind("air", "http://dig.csail.mit.edu/TAMI/2007/amord/air#")
		store.bind("owl", "http://www.w3.org/2002/07/owl#")
		
		if domain[-3:] == ".n3": #remove the n3 part and add the #
			domain_name = domain[:-3] 
			domain_chopped = domain.split("/")
			domain_prefix = domain_chopped[len(domain_chopped)-1]
			domain_name = domain_name + "#"
			store.bind( domain_prefix , domain_name)
		
		# Create namespace objects
		AIR = Namespace("http://dig.csail.mit.edu/TAMI/2007/amord/air#")
		OWL = Namespace("http://www.w3.org/2002/07/owl#")
		
		
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
		
		""" Add things to the pattern only if the sentence does not return null for each of the corresponding components"""
		if dict['ACTION'] == "use":
			pattern_1.add((URIRef("#U"), RDF.type, AIR["UseEvent"]))
		#elif: @todo: what else should be there?
		
		if dict['ENTITY'] != None:
			entity_match = getMatch(dict['ENTITY'],domain)
			pattern_1.add((URIRef("#U"), AIR["actor"], URIRef("#A")))
			if entity_match != None:
				pattern_1.add((URIRef("#A"), RDF.type, entity_match))
				
		if dict['DATA'] != None:
			data_match = getMatch(dict['DATA'], domain)
			pattern_1.add((URIRef("#U"), AIR["data"], URIRef("#D")))
			if data_match != None:
				pattern_1.add((URIRef("#D"), RDF.type, data_match))
	
		if dict['PURPOSE'] != None:
			purpose_match = getMatch(dict['PURPOSE'], domain)
			pattern_1.add((URIRef("#U"), AIR["purpose"], URIRef("#P")))
			if purpose_match != None:
				pattern_1.add((URIRef("#P"), RDF.type, purpose_match))
		
		if (dict.has_key('PASSIVE_ENTITY')):	
			if dict['PASSIVE_ENTITY'] != None:
				""" I think this is not even in the AIR specification 
				Therefore, @todo: Ask Lalana about this"""
				transferee_match = getMatch(dict['PASSIVE_ENTITY'], domain)
				pattern_1.add((URIRef("#A"), AIR["transfer"], URIRef("#D")))
				pattern_1.add((URIRef("#D"), AIR["transferred-to"], URIRef("#R")))
				if transferee_match != None:
					pattern_1.add((URIRef("#R"), RDF.type, transferee_match))
					
				
		totalConditions = len(dict['CONDITION'])
		if totalConditions != 0:
			conditions = dict['CONDITION']
			# create the rule body
			while (conditionCount < totalConditions):
				#Handle the conditions here
				if (conditions[conditionCount].subject[0] != '$'):
					matched_subject = getMatch(conditions[conditionCount].subject, domain)
				else:
					matched_subject = URIRef(getVariable(conditions[conditionCount].subject[1:]))
				
				if (conditions[conditionCount].predicate[0] != '$'):
					matched_predicate = getMatch(conditions[conditionCount].predicate, domain)
				else:
					matched_predicate = URIRef(getVariable(conditions[conditionCount].predicate[1:]))
				
				if (conditions[conditionCount].object[0] != '$'):
					matched_object = getMatch(conditions[conditionCount].object, domain)
				else:
					matched_object = URIRef(getVariable(conditions[conditionCount].object[1:]))
	
				conditionCount = conditionCount + 1
					
				if (matched_subject != None) and (matched_predicate != None) and (matched_object != None):
					#The terms should exist in the ontology or should be identified variables
					new_rule = "rule_"+conditionCount.__str__()
					new_rule = URIRef(new_rule)
					store.add((rule, AIR["rule"], new_rule))
					pattern = Graph()
					store.add((new_rule, AIR["pattern"], pattern))
					pattern.add((matched_subject, matched_predicate, matched_object))
							    
			
			""" Adding the assertion to the last rule  that was added"""
			assertion = Graph()
			store.add((new_rule, AIR["assert"], assertion))
			if dict['FLAG']:
				assertion.add((URIRef("#U"), AIR["compliant-with"], policy))
			else:
				assertion.add((URIRef("#U"), AIR["non-compliant-with"], policy))
		
		
		else:
			""" Adding the assertion to the first rule we created """
			assertion = Graph()
			store.add((rule, AIR["assert"], assertion))
			if dict['FLAG']:
			   assertion.add((URIRef("#U"), AIR["compliant-with"], policy))
			else:
				assertion.add((URIRef("#U"), AIR["non-compliant-with"], policy))
			
		""" @todo: support for air:description """	
				
		# Serialize as N3
		return store.serialize(format="n3")
	
