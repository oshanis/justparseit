"""
The main module for unification-based chart parsing.

The L{FeatureParser} class contains most of the code you would want to use.
"""

import nltk
import pdb
from nltk.cfg import *
from chart import *
from nltk.featstruct import *

def _override_repr(self):
    """
    Tweaks FeatStructNonterminals so that they display reasonably inside rules.
    """
    return self._repr(self._find_reentrances({}), {}).replace(']??',']/?').replace('/False', '')
cfg.FeatStructNonterminal.__repr__ = _override_repr
cfg.FeatStructNonterminal.__str__ = _override_repr

def _erase(featstruct):
    """
    Turns a FeatStructNonterminal into a plain Nonterminal, by discarding
    everything but the TYPE (the grammatical category).
    """
    # if it's actually a terminal string, return it
    if isinstance(featstruct, basestring): return featstruct

    # otherwise, turn it into a Nonterminal
    assert isinstance(featstruct[TYPE], basestring)
    return Nonterminal(featstruct[TYPE])

def erase_features(grammar, lexicon=None):
    """Given a feature-augmented grammar, produce an ordinary CFG by removing
    all features, leaving only grammatical categories."""

    prods = []
    for prod in grammar.productions():
        prod_erased = Production(_erase(prod.lhs()), [_erase(x) for x in prod.rhs()])
        prods.append(prod_erased)

    for word in grammar.lexicon():
        for tag in grammar.lexicon()[word]:
            prod_erased = Production(_erase(tag), [word])
            prods.append(prod_erased)
    for word in lexicon:
        for tag in lexicon[word]:
            prod_erased = Production(_erase(tag), [word])
            prods.append(prod_erased)
    
    return Grammar(_erase(grammar.start()), prods)

def correct_grammar(grammar):
    """
    Correct bugs in a grammar loaded by NLTK.
    
    NLTK 0.9 parses feature structures incorrectly, specifically when the
    SLASH feature's value is False or a variable.

    This function takes in a feature grammar (generally from an .fcfg file)
    parsed by NLTK, and modifies it _in place_ to properly handle values after
    a slash. It is run automatically in the parser.
    """
    for prod in grammar.productions():
        prod._lhs = _correct_featstruct(prod.lhs())
        prod._rhs = tuple(_correct_featstruct(r) for r in prod.rhs())
    return grammar

def _correct_featstruct(fstruct):
    """
    NLTK 0.9 parses feature structures incorrectly, specifically when the
    SLASH feature's value is True, False or a variable. This function turns
    misparsed feature structures into correct ones.
    """
    if not isinstance(fstruct, FeatStruct): return fstruct
    if fstruct.has_key(SLASH):
        if isinstance(fstruct[SLASH], FeatStruct):
            if repr(fstruct[SLASH])[0] == '?':
                newf = fstruct.copy()
                newf[SLASH] = Variable(str(fstruct[SLASH])[0:-2])
                return newf
            elif repr(fstruct[SLASH]) == 'True[]':
                newf = fstruct.copy()
                newf[SLASH] = True
                return newf
            elif repr(fstruct[SLASH]) == 'False[]':
                newf = fstruct.copy()
                newf[SLASH] = False
                return newf
    return fstruct

def remove_nullary(grammar):
    """
    Given a grammar, return an equivalent grammar with no nullary productions.

    When running the parse with features erased, we want to use a simple
    bottom-up parsing strategy. This won't work if we need there to be
    zero-length edges in the parse, which would arise from rules with nothing
    on the right-hand side. This function, then, rewrites the grammar so that
    such edges will not be necessary.
    """
    prods = grammar.productions()
    newprods = [p for p in prods + _remove_nullary_many(prods, prods) if p.rhs()]
    return Grammar(grammar.start(), newprods, grammar.lexicon())

def _remove_nullary_many(allprods, checkprods):
    newprods = []
    for prod in checkprods:
        newprods.extend(_remove_nullary_single(allprods, prod))
    if newprods: return newprods + _remove_nullary_many(allprods, newprods)
    else: return []

def _remove_nullary_single(prods, thisprod):
    if len(thisprod.rhs()) > 0: return []
    newprods = []
    lhs = thisprod.lhs()
    for nextprod in prods:
        rhs = nextprod.rhs()
        for i in range(len(rhs)):
            bindings = {}
            if unify(rhs[i], lhs, bindings):
                newprod = Production(
                  substitute_bindings(nextprod.lhs(), bindings),
                  [substitute_bindings(r, bindings) for r in rhs[:i]] +
                  [substitute_bindings(r, bindings) for r in rhs[i+1:]])
                newprods.append(newprod)
                #print "Was:", nextprod
                #print "Now:", newprod
    if newprods: return newprods + _remove_nullary_single(newprods, thisprod)
    else: return []

def _match_nonterminals(edge, fprod):
    """Can this edge, with its features erased, match a given feature
    production?"""

    if edge.lhs().symbol() != fprod.lhs()[TYPE]: return False
    result = edge.rhs() == tuple(_erase(x) for x in fprod.rhs())
    return result

def _isTerminalEdge(edge):
    """Does this edge have a word as its right-hand side?"""
    return edge.rhs() and isinstance(edge.rhs()[0], basestring)

class FeatureParser(object):
    """
    A chart parser that handles feature structures efficiently.
    
    This parser works by first running a chart parse with all the features
    except the part of speech removed. (Variables and unspecified values are
    not allowed in the part of speech.) Then, when constructing the parse
    trees to output, it uses the complete grammar with features, so that
    it only outputs trees with a consistent feature assignment.

    The following is an example of setting up and running the parser,
    including interfacing with the Kimmo algorithm for recognizing words:

    >>> import kimmo
    >>> g = nltk.data.load('file:gazdar.fcfg')
    >>> k = kimmo.load('gazdar.kimmo.yaml')
    >>> parser = FeatureParser(g, lexicon_func=kimmoScanner(k), trace=2)
    >>> sentence = "The kennel which Fido sleeps in has been stolen"    
    >>> for p in parser.parse_sentence(sentence):
    ...     print p

    (Start[]
      (S[+fin]
        (NP[agr=[person=3, -plural], -wh]
          (NP[agr=[person=3, -plural], -wh]
            (DET[agr=?a, -wh] The)
            (NBAR[agr=[person=3, -plural], -wh]
              (N[agr=[person=3, -plural], -wh] kennel)))
          (R[-wh]
            (RCOMP[+wh] which)
            (S[+fin]/NP[wh=?w]
              (NP[agr=[person=3, -plural], -wh]
                (NAME[agr=[person=3, -plural]] Fido))
              (VP[agr=[person=3, -plural, tense='present'], +fin]/NP[wh=?w]
                (V[agr=[person=3, -plural, tense='present'], class='C', +fin]
                  sleeps)
                (PP[wh=?w]/NP[wh=?w] (P[] in))))))
        (AUX[agr=[person=3, -plural, tense='present'], +fin]
          (HAVEP[agr=[person=3, -plural, tense='present']]
            (HAVE[agr=[person=3, -plural, tense='present'], +fin] has))
          (BEP[agr=[tense='past']] (BE[agr=[tense='past'], +fin] been)))
        (XP[]
          (VP[agr=[tense='past'], +fin]
            (V[agr=[tense='past'], class='C', +fin] stolen)))))
    
    To make parse trees more comprehensible, you may want to pass them to
    the included TreeView class, which displays them in a Tk window:

    >>> from treeview import TreeView
    >>> trees = parser.parse_sentence(sentence)
    >>> TreeView(trees)
    """

    def __init__(self, grammar, lexicon_func=None, trace=0):
        """
        Set up the parser.

        This constructor takes the following parameters:
        
        @param grammar: An NLTK grammar whose rules consist of
        FeatStructNonterminals. Such a grammar can be created by using
        nltk.data.load on a file with the extension .fcfg. Some examples are
        in this directory.
        
        @param lexicon_func: An optional function that assigns parts of speech
        to words. If no lexicon_func is provided, then productions in the
        grammar such as N -> 'dog' can fulfill the same purpose.

        @param trace: Sets the level of output to show. As the number
        increases, the parser provides an increasing amount of output that
        can be used for debugging.
          0: No output.
          1: Announce each phase of parsing with a status message.
          2: Also show a representation of the edges being produced by the
             bottom-up parser.
          3: Also show when features are successfully assigned to an edge,
             in the feature-assignment phase that occurs after parsing.
          4: When features are successfully assigned to an edge, also show
             the subtree constructed so far. (This produces a lot of output.)
          5: Also show when feature assignment fails.
          6: During feature assignment, show each edge and the list of possible
             subtrees that arises from feature assignment.
        """

        self._grammar = grammar
        if trace > 1: print "Loading grammar..."
        correct_grammar(self._grammar)
        if trace > 1: print "Rewriting nullary productions..."
        self._grammar = remove_nullary(self._grammar)
        self._lexicon_func = lexicon_func
        self._trace=trace
    
    def parse_sentence(self, sentence):
        """
        Takes in a sentence, tokenizes it by whitespace, and returns the list
        of parses.

        Your situation may require a more sophisticated tokenizer, in which
        case you should pass the list of tokens to nbest_parse instead.
        """
        return self.nbest_parse(sentence.split())

    def nbest_parse(self, tokens, n=None):
        """
        Runs the parser on a list of tokens.

        The function is named nbest_parse for compatibility with other NLTK
        classes, but it will always return all the parses, ignoring n.
        """
        lexicon = self._build_lexicon(tokens)
        if lexicon is None: lexicon = self._grammar.lexicon()
        grammar = erase_features(self._grammar, lexicon)
        
        # inner parser
        chart = Chart(list(tokens))
        
        # Width, for printing trace edges.
        w = 50/(chart.num_leaves()+1)
        if self._trace > 0: print chart.pp_leaves(w)
        
        # Handle the lexicon
        for index in range(chart.num_leaves()):
            word = chart.leaf(index)
            for pos in lexicon.get(word, []) + lexicon.get(word.lower(), []):
                edge = TreeEdge((index, index+1), _erase(pos), [word], 1)
                leafedge = LeafEdge(word, index)
                chart.insert(leafedge, ())
                if chart.insert(edge, (leafedge,)):
                    if self._trace > 1: print chart.pp_edge(edge,w)
        
        # Parse bottom-up. This is the most reliable of NLTK's parsing
        # strategies, and runs about as fast as the Earley strategy even though
        # Earley should theoretically be faster.
        for strategy in [BU_STRATEGY]:
            edges_added = 1
            while edges_added > 0:
                edges_added = 0
                for rule in strategy:
                    edges_added_by_rule = 0
                    for e in rule.apply_everywhere(chart, grammar):
                        if self._trace > 0 and edges_added_by_rule == 0:
                            print '%s:' % rule
                        edges_added_by_rule += 1
                        if self._trace > 1: print chart.pp_edge(e,w)
                    if self._trace == 1 and edges_added_by_rule > 0:
                        print '  - Added %d edges' % edges_added_by_rule
                    edges_added += edges_added_by_rule
        
        # now assign features according to the full grammar
        if self._trace > 0: print 'Assigning features...'
        parses = self.assign_features(chart, grammar.start(), lexicon)
        return parses
    parse = nbest_parse

    def assign_features(self, chart, root, lex):
        """
        After the chart has been constructed, find the resulting parse
        trees while assigning features from the top down.
        """
        trees = []
        for edge in chart.select(span=(0, chart._num_leaves), lhs=root):
            trees += self._trees(chart, edge, lex, memo={}, unifymemo={})
        return trees

    def _trees(self, chart, edge, lex, memo, unifymemo):
        if edge in memo: return memo[edge]
        trees = []
        if edge.is_incomplete(): return trees
        memo[edge] = []
        if _isTerminalEdge(edge):
            word = chart.leaf(edge.start())
            for tag in lex[word]:
                if _erase(tag) == edge.lhs():
                    trees.append(Tree(tag, [word]))
            memo[edge] = trees
            return trees
        matched = False
        for prod in self._grammar.productions():
            if _match_nonterminals(edge, prod):
                matched = True
                for cpl in chart.child_pointer_lists(edge):
                    child_choices = [self._trees(chart, nextedge, lex, memo, unifymemo)
                                     for nextedge in cpl]
                    for children in chart._choose_children(child_choices):
                        bindings = {}
                        unified = True
                        # check for a feature match ...
                        newrhs = []
                        for pattern, tree in zip(prod.rhs(), children):
                            u = unify(pattern, tree.node, bindings)
                            if u is None:
                                unified = False
                                break
                            newtree = Tree(u, list(tree))
                            newrhs.append(newtree)
                        if unified:
                            lhs = substitute_bindings(prod.lhs(), bindings)
                            tree = Tree(lhs, newrhs)
                            trees.append(tree)
                            if self._trace > 2:
                                print ('.' * edge.start() + '=' * (edge.end() - edge.start()) + '.' * (chart.num_leaves() - edge.end())), tree.node
                                if self._trace > 3:
                                    print tree
                                    print
                        else:
                            tree = Tree(prod.lhs(), children)
                            if self._trace > 4 and len(tree.leaves()):
                                print 'Failed:', prod.rhs()
                                print ' unifying with:', tree
        if not matched:
            raise ValueError(edge)
        memo[edge] = trees
        if self._trace > 5:
            print 'Expanded:', edge
            print '  Result:', trees
        return trees

    def _build_lexicon(self, tokens):
        if self._lexicon_func is None: return None
        lexicon = {}
        for token in tokens:
            lexicon[token] = self._lexicon_func(token)
        return lexicon

def run_parser(grammarfile, kimmofile=None, gui=False, trace=0):
    """
    Run a parser interactively.
    
    This function takes in the filename of a grammar file,
    which should end in .fcfg, and optionally a Kimmo rule filename which
    should end in .yaml. 

    If given the option gui=True, it will display a Tk window of the resulting
    parse trees. trace= is an integer from 0 to 6 which controls how much
    output to show: trace=0 will only show the resulting parse trees, for
    example, while trace=3 shows a reasonable amount of output from parsing and
    feature unification.
    """
    if kimmofile: import kimmo
    grammar = nltk.data.load('file:'+grammarfile)
    if kimmofile is not None:
        kimmo_obj = kimmo.load(kimmofile)
        lexicon_func = kimmoScanner(kimmo_obj)
    else:
        lexicon_func = None
    parser = FeatureParser(grammar, lexicon_func, trace=trace)
    sentence = raw_input("Sentence: ")
    trees = parser.parse_sentence(sentence)
    for tree in trees:
        print tree
    if gui:
        view_trees(trees)

def kimmoScanner(kimmo):
    """
    Given a kimmo object, this returns a function that can be used as a
    lexicon function.

    It takes in a word, converts it to lowercase, and runs it through the
    Kimmo recognizer, returning all parts of speech or feature structures
    that the recognizer returns.
    """
    def scanner(word, kimmo=kimmo):
        return [r[1] for r in kimmo.recognize(word.lower())]
    return scanner

def view_trees(trees):
    """
    Display a list of trees in a Tk GUI window.
    """
    from treeview import TreeView
    TreeView(trees)

def demo():
    """
    This is the demo that runs when you run this file as a standalone script.
    """
    import kimmo
    g = nltk.data.load('file:gazdar.fcfg')
    k = kimmo.load('gazdar.kimmo.yaml')
    parser = FeatureParser(g, lexicon_func=kimmoScanner(k), trace=3)
    for p in parser.parse_sentence("The kennel which Fido sleeps in has been stolen"):
        print p

if __name__ == '__main__': demo()

