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
                'actedOn':'DATA', 'purpose':'PURPOSE', 
                'condition' : 'CONDITION', 'mod' : 'FLAG'}

CONCAT_OPERATOR = 'cat'
AND_OPERATOR = 'and'
TRUE_MOD = 'yes'
FALSE_MOD = 'no'
NULL_VALUE = 'null'

def isVariable(exp):
    return type(exp) == nltk.sem.logic.VariableExpression
    
def isApplication(exp):
    return type(exp) == nltk.sem.logic.ApplicationExpression

def isOperator(exp):
    return type(exp) == nltk.sem.logic.Operator

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

def parseSingleCondition(cond):
    
    #cond = (action actor) (actedOn)
    left = cond.first
    right = cond.second
    
    if isVariable(right) and isApplication(left):
        left_left = left.first
        left_right = left.second
        if isVariable(left_left) and isVariable(left_right):
            result = Cond(left_right.name(), left_left.name(), right.name())
        else:
            raise InvalidExpressionError(cond)            
    else:
        raise InvalidExpressionError(cond)

    return result

def traverseConditions(exp):

    if isApplication(exp):
        # check whether it's a single condition or multiple conditions
        left = exp.first
        right = exp.second

        #multiple conditions: cond = (and cond1) cond2
        if isApplication(left):
            left_left = left.first
            left_right = left.second
            if isOperator(left_left) and left_left.name() == AND_OPERATOR and isApplication(left_right):
                result = [parseSingleCondition(left_right)] + traverseConditions(right)
            else:
                result = [parseSingleCondition(exp)]
        else:
            raise InvalidExpressionError(exp)     
    elif isVariable(exp) and exp.name() == NULL_VALUE:
        # condition is optional, so it can be null
        result = None
    else:
        raise InvalidExpressionError(exp)
    
    return result

def traverseMod(exp):
    
    if isVariable(exp):
        val = exp.name()
        if (val == TRUE_MOD):
            result = True
        elif (val == FALSE_MOD):
            result = False
        else:
            raise InvalidExpressionError(exp)
    else:
        raise InvalidExpressionError(exp)
    
    return result

def parseSemantics(tree):
    
    node = tree.node
    policy_dict = {}
    
    for key in CFG2RDF_DICT:
        if (key == 'condition'):
            value = traverseConditions(node[key])
        elif (key == 'mod'):
            value = traverseMod(node[key])
        else:
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
        return None
    elif num_parses > 1:
        print 'Warning: More than one parses for this policy!'
    
    """
    Extract the Actor, Action, ActedOn, Purpose, and Condition 
    from the parse tree.
    They are simply leaf nodes in the tree.
    """
    tree = trees[0]
    
    try:
        policy_dict = parseSemantics(tree)
        policy_dict['POLICY'] = policy_name
        return policy_dict
    except InvalidExpressionError, e:
        print "Could not parse the expression:" + e.value.__str__()
    
    return None

def run():
    """
    The main method for the policy parser
    """ 
    policy_name = raw_input("Enter the name of a policy: ")
    policy_sentence = raw_input("Enter the policy sentence: ")
   
    policy_dict = parsePolicy(policy_name, policy_sentence)
    
    print policy_dict
 
if __name__ == '__main__': # What else would it be?
    run()
