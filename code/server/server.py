#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp

def main():
    
    name = "MITProxCardDataPolicy"
    #sentence = "MIT can use prox card data for criminal investigation"
    sentence = "MIT can use prox card data for criminal investigation if MIT has authorization"
    domain = "http://www.mit.edu/~oshani/data/university.n3"
    domain_name = "MIT"
    
    dict = parseNL(name, sentence)

    returnString = constructPolicy(dict, domain, domain_name)
    
    print returnString
    


if __name__ == '__main__': # What else would it be?
    
    import sys
    
    sys.path.append("../PolicyParser/")
    sys.path.append("../featureparse")
    sys.path.append("../RDFGenerator")

    from generate import *
    from pparser import *
    from Condition import *
    
    main()
    
