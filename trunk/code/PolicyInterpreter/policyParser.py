"""
6.863 Spring 2008 Project

The Policy Parser
"""

from policyInterpreter import *

GRAMMAR_FILE = 'file:../data/grammar.fcfg'
KIMMO_FILE = '../data/gazdar.kimmo.yaml'

"""
    Given multiple syntax trees from an input sentence, pick the one
    with the least number of null features
    ("purpose" and "passiveEntity" are optional - look for parse trees that
        contain non-null values for these features)
"""
def pickMostLikelyParse(trees):
    
    tree = trees[0]
    
    for curTree in trees:
        oldNode = tree.node
        curNode = curTree.node
        if isNullFeature(oldNode['purpose']) and not isNullFeature(curNode['purpose']):
            tree = curTree
       
        if isNullFeature(oldNode['passiveEntity']) and not isNullFeature(curNode['passiveEntity']):
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

    parser = FeatureParser(grammar, lexicon_func, trace=3)
   
    # parse the sentence into a syntax tree(s) using featureparser
    trees = parser.parse_sentence(policy_sentence)
    num_parses = len(trees)

    if num_parses == 0:
        print 'Error: Could not parse this policy!'
        return None
    elif num_parses > 1:
        print 'Warning: More than one parses for this policy!'
    
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
        print "Could not interpret the expression:" + e.value.__str__()
        return None
  
    return policy_dict
 
"""
    The main method for the policy parser
"""    
def run():
    policy_name = raw_input("Enter the name of a policy: ")
    policy_sentence = raw_input("Enter the policy sentence: ")
   
    policy_dict = parsePolicy(policy_name, policy_sentence)
   
    print policy_dict

#if __name__ == '__main__': # What else would it be?
run()
