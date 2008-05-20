#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp

def main():
    
    name = "MITProxCardDataPolicy"
    #sentence = "MIT can use prox card data for criminal investigation"
    sentence = "mit may use prox card data for criminal investigation"
    domain = "../data/ontology.n3"
    
    dict = parseNL(name, sentence)
    print dict
    returnString = constructPolicy(dict, domain)
    
    print returnString
    


if __name__ == '__main__': # What else would it be?
    
    import sys
    
    sys.path.append("../PolicyInterpreter")
    sys.path.append("../featureparse")
    sys.path.append("../RDFGenerator")

    from generate import *
    from policyParser import *
    from condition import *
    
    main()
    
