"""
6.863 Spring 2008 Project

The Policy Parser
"""

from featureparse import *
from Condition import *

CFG2RDF_DICT = {'Policy':'POLICY', 'Actor':'ENTITY', 'Action':'ACTION', 
                'ActedOn':'DATA', 'Purpose':'PURPOSE', 'Condition':'CONDITION'}

def parsePolicy(policy_name, policy_sentence):
 
    grammar_file = 'simple.fcfg'
    grammar = nltk.data.load('file:../data/'+grammar_file)
    kimmo_file = None
    lexicon_func = None
    parser = FeatureParser(grammar, lexicon_func, trace=0)
   
    # parse the sentence into a tree(s)
    trees = parser.parse_sentence(policy_sentence)
    num_parses = len(trees)

    if num_parses == 0:
        print 'Error: Could not parse this policy!'
        return
    elif num_parses > 1:
        print 'Warning: More than one parses for this policy!'
    
    """
    Extract the Actor, Action, ActedOn, Purpose, and Condition 
    from the parse tree.
    They are simply leaf nodes in the tree.
    """
    parts = trees[0].pos()
    policy_dict = {'POLICY' : policy_name}
    
    #TODO: remove the fake condition - for testing only
    cond = AndCond(AtomicCond('authorized'), AtomicCond('has_permission'))
    policy_dict['CONDITION'] = cond
    policy_dict['FLAG'] = True
    
    # Create a dictionary entry for each of the four parts 
    for cur_part in parts:
        value = cur_part[0]
        key = cur_part[1].values().pop()
        if key == 'AuxNegative':
            policy_dict['FLAG'] = False
        elif key == 'AuxPositive':
            policy_dict['FLAG'] = True
        elif key != 'Prop':
            policy_dict[CFG2RDF_DICT[key]] = value
       
    return policy_dict

def run():
    """
    The main method for the policy parser
    """ 
    policy_name = raw_input("Enter the name of a policy: ")
    policy_sentence = raw_input("Enter the policy sentence: ")
   
    policy_dict = parsePolicy(policy_name, policy_sentence)
    
    print policy_dict
 
 #Commented by Oshani  
#run()
