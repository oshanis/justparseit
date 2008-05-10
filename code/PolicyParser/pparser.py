"""
6.863 Spring 2008 Project

The Policy Parser
"""

from featureparse import *
from Condition import *

class InvalidExpressionError(Exception):
    def __init__(self, value):
        self.value = value

CFG2RDF_DICT = {'actor':'ENTITY', 'action':'ACTION',
                'actedOn':'DATA', 'purpose':'PURPOSE'}

CONCAT_OPERATOR = 'cat'

def isVariable(exp):
    return type(exp) == nltk.sem.logic.VariableExpression
    
def isApplication(exp):
    return type(exp) == nltk.sem.logic.ApplicationExpression

def processAppExpression(appExp):
    left = appExp.first
    right = appExp.second

#    print 'left:' + left.__str__()
#    print 'right:' + right.__str__()

    #exp = ((cat X) Y)
    if isApplication(left):
        
        left_left = left.first
        left_right = left.second 
        
        if isVariable(left_left) and isVariable(left_right) and left_left.name() == CONCAT_OPERATOR:
            
            left_value = left_right.name()  #X
            right_value = traverseExpression(right) #Y
            
            result = left_value + ' ' + right_value
            
        else:
            raise InvalidExpressionError(appExp)
    else: 
        raise InvalidExpressionError(appExp)
    
    return result

def traverseExpression(exp):
    
#    print 'exp:' + exp.__str__()
          
    if isApplication(exp):  
        result = processAppExpression(exp)
    elif isVariable(exp):
        result  = exp.name()
    else:
        raise InvalidExpressionError(exp)
       
    return result
    
def parseSemantics(tree):
    
    node = tree.node
    policy_dict = {}
    
    for key in CFG2RDF_DICT:
        value = traverseExpression(node[key])
        policy_dict[CFG2RDF_DICT[key]] = value
        
    return policy_dict

def parsePolicy(policy_name, policy_sentence):
 
    grammar_file = 'grammar.fcfg'
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
