"""
6.863 Spring 2008 Project

The Policy Parser
"""

from featureparse import *

def run():
    """
    The main method for the policy parser
    """

    grammar_file = 'simple.fcfg'
    grammar = nltk.data.load('file:'+grammar_file)
    kimmo_file = None
    lexicon_func = None
    
    parser = FeatureParser(grammar, lexicon_func, trace=0)
    sentence = raw_input("Enter a policy: ")
    
    # parse the sentence into a tree(s)
    trees = parser.parse_sentence(sentence)
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
    
    for cur_part in parts:
        print cur_part

    return

run()
