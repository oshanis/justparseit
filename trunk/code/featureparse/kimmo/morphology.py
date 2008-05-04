"""
This module handles the special finite state transducer that represents a language's lexicon.
"""

from fsa import FSA
import yaml
from nltk.featstruct import *

def startswith(stra, strb):
    return stra[:len(strb)] == strb

def endswith(stra, strb):
    return strb == '' or stra[-len(strb):] == strb

def combine_features(a, b):
    """
    Return an object that combines the feature labels a and b.
    
    If a and b are strings, they are combined by concatenation (as in
    the original PC-KIMMO). If they are feature structures, then they
    are unified in a way that always succeeds: the newer structure, b,
    wins all conflicts.
    """
    def override_features(a, b, stuff):
        return b
    if a is None: return b
    if b is None: return a
    if isinstance(b, FeatStruct):
        if isinstance(a, FeatStruct):
            return unify(a, b, fail=override_features)
        else:
            return unify(FeatStructParser().parse(a), b, fail=override_features)
    else:
        return '%s%s' % (a, b)

class KimmoMorphology(object):
    def __init__(self, fsa):
        self._fsa = fsa
    def fsa(self): return self._fsa
    def valid_lexical(self, state, word, alphabet):
        trans = self.fsa()._transitions[state]
        for label in trans.keys():
            if label is not None and label[0].startswith(word) and len(label[0]) > len(word):
                next = label[0][len(word):]
                for pair in alphabet:
                    if next.startswith(pair.input()): yield pair.input()
    def next_states(self, state, word):
        choices = self.fsa()._transitions[state]
        for (key, value) in choices.items():
            if key is None:
                if word == '':
                    for next in value: yield (next, None)
            else:
                if key[0] == word:
                    for next in value:
                        yield (next, key[1])
                    
    @staticmethod
    def load(filename):
        f = open(filename)
        result = KimmoMorphology.from_text(f.read())
        f.close()
        return result
    @staticmethod
    def from_text(text):
        fsa = FSA([], {}, 'Begin', ['End'])
        state = 'Begin'
        for line in text.split('\n'):
            line = line.strip()
            if not line or line.startswith(';'): continue
            if line[-1] == ':':
                state = line[:-1]
            else:
                if line.split()[0].endswith(':'):
                    parts = line.split()
                    name = parts[0][:-1]
                    next_states = parts[1:]
                    for next in next_states:
                        fsa.insert_safe(name, None, next)
                elif len(line.split()) > 2:
                    # this is a lexicon entry
                    word, next, features = line.split(None, 2)
                    if word.startswith('"') or\
                    word.startswith("'") and word.endswith("'"):
                        word = eval(word)
                    if features:
                        if features == 'None':
                            features = FeatStruct()
                            features.freeze()
                        elif features.endswith(']'):
                            features = FeatStructParser().parse(features)
                            features.freeze()
                    if features == '': raise ValueError(line)
                    fsa.insert_safe(state, (word, features), next)
                elif len(line.split()) == 2:
                    word, next = line.split()
                    features = ''
                    if word == "''":
                        word = ''
                    fsa.insert_safe(state, (word, features), next)
                else:
                    print "Ignoring line in morphology: %r" % line
        return KimmoMorphology(fsa)
    def __str__(self):
        return yaml.dump(self._fsa)

def demo():
    print KimmoMorphology.load('../gazdar.kimmo.lex')

if __name__ == '__main__':
    demo()
