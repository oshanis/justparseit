"""
6.863 Spring 2008 Project

The Policy Parser
"""
import sys

sys.path.append('../featureparse/')
sys.path.append('../RDFGenerator/')
   
from policyInterpreter import *
from generate import *

GRAMMAR_FILE = 'file:../data/grammar.fcfg'
KIMMO_FILE = '../data/gazdar.kimmo.yaml'

"""
    Given multiple syntax trees from an input sentence, pick the one
    with the least number of null features
    ("passiveEntity" is optional - look for parse trees that
        contain non-null values for this feature)
"""
def pickMostLikelyParse(trees):
    
    tree = trees[0]
    
    for curTree in trees:
        oldNode = tree.node
        curNode = curTree.node
        if isNullFeature(oldNode['purpose']) and not isNullFeature(curNode['purpose']):
            tree = curTree
     
    return tree


"""
    Parses the input policy using the NTLK parser and
    extracts the semantic information about the policy
"""  
def parsePolicy(policy_name, policy_sentence):

    """
        To create a FCFG parser, we need the grammar (.fcfg), 
        the lexicon (.lex), and the spelling change rules (Kimmo file)
    """
    grammar = nltk.data.load(GRAMMAR_FILE)
   
    import kimmo
   
    if KIMMO_FILE is not None:
        kimmo_obj = kimmo.load(KIMMO_FILE)
        lexicon_func = kimmoScanner(kimmo_obj)
    else:
        lexicon_func = None

    parser = FeatureParser(grammar, lexicon_func, trace=0)
   
    # parse the sentence into a syntax tree(s) using featureparser
    trees = parser.parse_sentence(policy_sentence)
    num_parses = len(trees)

    if num_parses == 0:
        print ""
        print "Policy Parser Error: Could not parse this policy!"
        print "You are probably entering a sentence that does not fit the following structure:"
        print "subject [mod] action object ['to' secondary_object] ['for' purpose] [condition]*"
        return None
    
    # if there are multiple parses, pick the most likely one
    tree = pickMostLikelyParse(trees)

    try:
        """
        Extract the various policy constituents 
        (actor, action, actedOn, conditions, purpose, passive entity)
        from the parse tree.
        """
        policy_dict = interpretPolicy(tree)
        policy_dict['POLICY'] = policy_name
    except InvalidExpressionError, e:
        print ""
        print "Policy Parser Error: Could not interpret this policy!" 
        print "You are probably entering words that are not a part of the lexicon."
        return None
  
    return policy_dict
 
"""
    The main method for the policy parser
"""    
def runPolicyParser():
 
    domain = "http://www.mit.edu/~oshani/data/university.n3"
   
    policy_name = raw_input("Enter the name of a policy: ")
    policy_sentence = raw_input("Enter the sentence for the policy: ")
   
    policy_dict = parsePolicy(policy_name, policy_sentence)
    rdf = constructPolicy(policy_dict, domain)
     
    print ""
    print "The Policy Parser has generated the following RDF:"
    print rdf
    
    return rdf
    
if __name__ == '__main__': # What else would it be?
    runPolicyParser()
