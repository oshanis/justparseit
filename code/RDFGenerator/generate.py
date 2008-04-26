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

# create the policy
policy = URIRef("#MITProxCardPolicy")
store.add((policy, RDF.type, AIR["Policy"]))

#add the variables
store.add((policy, AIR["variable"], URIRef("#U")))
store.add((policy, AIR["variable"], URIRef("#D")))
store.add((policy, AIR["variable"], URIRef("#P")))

#add the outer rule
outer_rule = BNode()
store.add((policy, AIR["rule"], outer_rule))

outer_rule_pattern = Graph()
outer_rule_pattern.add((URIRef("#U"), RDF.type, AIR["UseEvent"]))
outer_rule_pattern.add((URIRef("#U"), AIR["data"], URIRef("#D")))
outer_rule_pattern.add((URIRef("#U"), AIR["purpose"], URIRef("#P")))
outer_rule_pattern.add((URIRef("#D"), RDF.type, MIT["ProxCardEvent"]))

store.add((policy, AIR["pattern"], outer_rule_pattern))

#create the rule body
store.add((outer_rule, AIR["label"], Literal("MIT prox-card policy")))
store.add((outer_rule, AIR["pattern"], Literal("MIT prox-card policy")))

# Serialize the store as RDF/XML to the file foaf.rdf.
store.serialize("policy.n3", format="n3", max_depth=3)

# Serialize as N3
print store.serialize(format="n3")

