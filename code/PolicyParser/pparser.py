"""
6.863 Spring 2008 Project

The Policy Parser
"""

from featureparse import *
from Condition import *

class InvalidExpressionError(Exception):
    def __init__(self, value):
        self.value = value

CFG2RDF_DICT = {'Policy':'POLICY', 'Actor':'ENTITY', 'Action':'ACTION', 
                'ActedOn':'DATA', 'Purpose':'PURPOSE', 'Condition':'CONDITION'}

SEM_FEATURE_KEYWORD = 'sem'

def isVariable(exp):
    return type(exp) == nltk.sem.logic.VariableExpression
    
def isApplication(exp):
    return type(exp) == nltk.sem.logic.ApplicationExpression

def isOperator(exp):
    return type(exp) == nltk.sem.logic.Operator

def processAppExpression(appExp):
    left = appExp.first
    right = appExp.second

    if isVariable(left) and isVariable(right):
        leftVar = left.name()
        rightVar = right.name()

        if leftVar in CFG2RDF_DICT:
            result = {CFG2RDF_DICT[leftVar] : rightVar}
        else:
            result = {}
    else: 
        #traverse the two sub-expressions and merge the resulting dictionaries
        dict_left = traverseExpression(left)
        dict_right = traverseExpression(right)
        dict_left.update(dict_right)
        result = dict_left
    
    return result
    
def traverseExpression(exp):
   
    result = {}
   
    if isApplication(exp):  
        result = processAppExpression(exp)
    elif isVariable(exp) or isOperator(exp):
        result = {}
    else:
        raise InvalidExpressionError(exp)
       
    return result
    
def parseSemantics(tree):
    
    exp = tree.node[SEM_FEATURE_KEYWORD]
    
    policy_dict = {}
    
    try:
        policy_dict = traverseExpression(exp)
    except InvalidExpressionError, e:
        print 'Failed to interpret the semantics: ', e.value
        ploicy_dict = {}
        
    return policy_dict

def parsePolicy(policy_name, policy_sentence):
 
    grammar_file = 'simple2.fcfg'
    grammar = nltk.data.load('file:../data/'+grammar_file)
    kimmofile = 'gazdar.kimmo.yaml'
   
    import kimmo
   
    if kimmofile is not None:
        kimmo_obj = kimmo.load('../data/'+kimmofile)
        lexicon_func = kimmoScanner(kimmo_obj)
    else:
        lexicon_func = None
    
    parser = FeatureParser(grammar, lexicon_func, trace=3)
   
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
    tree = trees[0]

    policy_dict = parseSemantics(tree)
    
    policy_dict['POLICY'] = policy_name
    
    #TODO: remove the fake condition - for testing only
    cond1 = Cond('mit', 'is', 'authorized')
    cond2 = Cond('harshad', 'gives', 'treats')
    cond3 = Cond('oshani', 'has', 'permission')
    policy_dict['CONDITION'] = [cond1, cond2, cond3]
    policy_dict['FLAG'] = True
           
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
run()
