from featureparse import *
from nltk.sem.logic import Counter, ApplicationExpression, Variable, VariableExpression
import sys, string

"""
This is some experimental code that you can use to interact with a grammar
with semantic features.
"""

def object_to_features(obj):
    """
    Represent an arbitrary Python object as a feature structure (NLTK class
    FeatStruct).

    This is a messy but effective way to unify objects which may contain
    Variables, and which could not normally be unified using FeatStruct.unify.
    Semantic objects such as ApplicationExpressions are examples of this.
    """

    if not hasattr(obj, '__dict__'): return obj
    if str(obj).startswith('?'):
        return Variable(str(obj)[1:])
    if isinstance(obj, FeatStruct): return obj
    if isinstance(obj, dict): return FeatStruct(obj)
    thedict = {}
    thedict['__class__'] = obj.__class__.__name__
    for (key, value) in obj.__dict__.items():
        thedict[key] = object_to_features(value)
    return FeatStruct(thedict)

def interact(grammar_filename, trace=2):
    """This is the main loop of interaction, prompting the user for a sentence
    and using the semantic features to give a response. grammar_filename
    should be in nltk.data.load style, so it should look like 'file:slash.fcfg'.
    """
    grammar = nltk.data.load(grammar_filename)
    cp = FeatureParser(grammar, trace=trace-2)
    
    model = []
    counter = Counter()
    while True:
        sys.stdout.write('> ')
        line = sys.stdin.readline().strip()
        if not line: break

        # Read a line and parse it.
        trees = cp.parse_sentence(line.lower())
        if len(trees) == 0:
            print "I don't understand."
            continue
        elif len(trees) > 1:
            print "That was ambiguous, but I'll guess at what you meant."
        
        # Extract semantic information from the parse tree.
        tree = trees[0]
        pos = tree[0].node[TYPE]
        sem = tree.node['sem']

        # We need variables to have unique names even if they didn't get
        # alpha-converted already. Replace all the variables that are unbound
        # via skolemization -- but not the ones that are completely free,
        # like "mary" -- with uniquely-named ones.
        free = sem.free()
        skolem = sem.skolemize()
        almostfree = skolem.free()
        vars = set(almostfree).difference(free)
        for var in vars:
            skolem = skolem.replace_unique(var, counter)
        
        if trace > 0:
            print tree
            print 'Semantic value:', skolem
        clauses = skolem.clauses()
        if trace > 1:
            print "Got these clauses:"
            for clause in clauses:
                print '\t', clause
        
        if pos == 'S':
            # Handle statements
            model += clauses
            print 'Okay.'
        elif pos == 'Q':
            # Handle questions
            bindings = {}
            success = True
            for clause in clauses:
                success = False
                for known in model:
                    newbindings = dict(bindings)
                    feat1 = object_to_features(clause)
                    feat2 = object_to_features(known)
                    if unify(feat1, feat2, newbindings):
                        bindings = newbindings
                        success = True
                        break
                if not success:
                    break
            if success:
                answer = 'Yes.'
                # look for bindings starting with ?wh -- the variable might
                # have been renamed
                for key, value in bindings.items():
                    if str(key).startswith('wh'):
                        answer = value
                print outputEnglish(answer, model)
            else:
                # This is an open world without negation, so negative answers
                # aren't possible.
                print "I don't know."

def outputEnglish(answer, model):
    """
    What we have at this point is a Python object mangled into a feature
    structure. Let's attempt to turn it into English text.
    """
    if isinstance(answer, FeatStruct):
        varname = answer['variable']['name']
        
        # Constants are unbound variables that begin with capital letters
        if varname and varname[0] in string.letters.upper():
            return varname
        
        # If it's not a constant, search for a description of it
        clause = ApplicationExpression(VariableExpression(Variable('?desc')), VariableExpression(Variable(varname)))
        for known in model:
            bindings = {}
            feat1 = object_to_features(clause)
            feat2 = object_to_features(known)
            if unify(feat1, feat2, bindings):
                varanswer = bindings[Variable('desc')]
                return 'the ' + varanswer['variable']['name']
    else: return answer


def demo():
    """Run the interaction loop on a grammar."""
    import sys
    if len(sys.argv) > 1:
        filename = 'file:'+sys.argv[1]
    else:
        print "No filename given; demoing on semantics.fcfg."
        filename = 'file:semantics.fcfg'
    interact(filename, trace=5)

if __name__ == '__main__':
    demo()

