"""
6.863 Spring 2008 Project

The Policy Interpreter
- Extracts semantic information from a syntax tree that corresponds to a policy
"""

from featureparse import *
from condition import *
from policyParserExceptions import *

""" 
    Beginning of Constants
"""
CFG2RDF_DICT = {'actor':'ENTITY', 'action':'ACTION',
                'actedOn':'DATA', 'purpose':'PURPOSE', 
                'condition' : 'CONDITION', 'mod' : 'FLAG',
                'passiveEntity': 'PASSIVE_ENTITY'}

CONCAT_OPERATOR = 'cat'
AND_OPERATOR = 'and'
STR_OF = 'of'
STR_PURPOSE = 'purpose'
TRUE_MOD = 'yes'
FALSE_MOD = 'no'
NULL_VALUE = 'null'

"""
    End of Constants
"""

def isVariable(exp):
    return type(exp) == nltk.sem.logic.VariableExpression
    
def isApplication(exp):
    return type(exp) == nltk.sem.logic.ApplicationExpression

def isOperator(exp):
    return type(exp) == nltk.sem.logic.Operator

""" 
    Check whether a feature is null
    A null feature is assigned '<null>'
"""
def isNullFeature(feature):
    return isVariable(feature) and feature.name() == NULL_VALUE
      
"""
    Process a function application expression
    The expression must be a curried application of 'cat'
    to two sub-expressions
"""
def processAppExpression(appExp):
    left = appExp.first
    right = appExp.second

    #print "left:" + left.__str__()
    #print "right:" + right.__str__()

    # exp = ((cat X) Y)
    if isApplication(left):
        
        left_left = left.first
        left_right = left.second 
        
        if isVariable(left_left) and left_left.name() == CONCAT_OPERATOR:
            
            if isVariable(left_right): 
                left_value = left_right.name()  #X
            else:
                left_value = traverseExpression(left_right)
          
            # special case: if the phrase is "purpose of Z", then strip off "purpose of"
            if left_value == STR_PURPOSE:
                if isApplication(right) and right.first.second.name() == STR_OF:
                    result = traverseExpression(right.second)
                else:
                    raise InvalidExpressionError(appExp)
            else:
                right_value = traverseExpression(right) #Y
                result = left_value + ' ' + right_value
            
        else:
            raise InvalidExpressionError(appExp)
    else: 
        raise InvalidExpressionError(appExp)
    
    return result

"""
    Traverse a logical (i.e. lambda-calculus) expression that represents a feature
    and returns a string representation of the expression, to be stored as the value
    to a particular policy constituent
"""
def traverseExpression(exp):
    
    #print "exp:" + exp.__str__()
    
    if isApplication(exp):  
        result = processAppExpression(exp)
    elif isVariable(exp):
        result  = exp.name()
        if result == NULL_VALUE:
            result = None
    else:
        raise InvalidExpressionError(exp)
       
    return result

"""
    Match "token" against any of the keys in
    "policy_dict". If there is a match, then 
    prepend the character '$' to the key and return it. 
"""
def matchTokenInDict(token, policy_dict):
    
    for key in policy_dict:
        val = policy_dict[key]
        if val == token:
            return '$' + key
    
    return token

"""
    Extract subject-predicate-object information from
    an expression that corresponds to a single condition.
    Returns an instance of class Cond.
"""      
def interpretSingleCondition(cond, policy_dict):
    
    #cond = (action actor) (actedOn)
    left = cond.first
    right = cond.second
    
    if isApplication(left):
        left_left = left.first
        left_right = left.second
        
        subject = matchTokenInDict(traverseExpression(left_right), policy_dict)
        predicate = matchTokenInDict(traverseExpression(left_left),policy_dict)
        object = matchTokenInDict(traverseExpression(right), policy_dict)
        
        result = Cond(subject, predicate, object)
    else:
        raise InvalidExpressionError(cond)

    return result

"""
    Traverse the expression corresponding to the condition feature
    The feature may contain multiple conditions, concatenated using
    the logical "and" operator.
"""
def traverseConditions(exp, policy_dict):

    if isApplication(exp):
        # check whether it's a single condition or multiple conditions
        left = exp.first
        right = exp.second

        #multiple conditions: cond = (and cond1) cond2
        if isApplication(left):
            left_left = left.first
            left_right = left.second
            if isOperator(left_left) and left_left.name() == AND_OPERATOR and isApplication(left_right):
                result = [interpretSingleCondition(left_right, policy_dict)] + traverseConditions(right, policy_dict)
            else:
                result = [interpretSingleCondition(exp, policy_dict)]
        else:
            raise InvalidExpressionError(exp)     
    elif isVariable(exp) and exp.name() == NULL_VALUE:
        # condition is optional, so it can be null
        result = []
    else:
        raise InvalidExpressionError(exp)
    
    return result

"""
    Extract the modality information
    Return True if it's a positive modality ("can", "may")
            False if it's a negative one ("cannot", "may not")
"""
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

"""
    Given a parse tree, extract policy constituents, 
    and return a dictionary that contains the list of key-pair
    values for the constituents
"""
def interpretPolicy(tree):
    
    node = tree.node
    policy_dict = {}
    
    for key in CFG2RDF_DICT:
   
        if (key == 'condition'):
            # skip conditions for now
            continue
        elif (key == 'mod'):
            # modality is a special case
            value = traverseMod(node[key])
        else:
            value = traverseExpression(node[key])
        
        policy_dict[CFG2RDF_DICT[key]] = value
    
    """    
        Conditions should be parsed as the last,
        because they depend on the previous entries in the dictionary
    """
  
    value = traverseConditions(node['condition'], policy_dict)
    policy_dict[CFG2RDF_DICT['condition']] = value
       
    return policy_dict
