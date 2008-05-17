#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp

def main():
    
    name = "MITProxCardDataPolicy"
    #sentence = "MIT can use prox card data for criminal investigation"
    sentence = "MIT can use prox card data for criminal investigation"
    domain = "../data/university.n3"

    dict = parseNL(name, sentence)

    returnString = constructPolicy(dict, domain)
    #returnString = returnString.encode('utf_8')
    print "Content-type:text/html\n"
    print "<html>"+returnString+"</html>"
    


if __name__ == '__main__': # What else would it be?
    
    import sys
    
    sys.path.append("../PolicyParser/")
    sys.path.append("../featureparse")
    sys.path.append("../RDFGenerator")

    from generate import *
    from pparser import *
    from Condition import *
    
    print "Content-type:text/html\n"
    

    main()
    
