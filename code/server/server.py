#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp

def main():
    
    name = "MITProxCardDataPolicy"
    
    #sentence = "MIT can use prox card data for criminal investigations"
    #sentence = "a person may access data on the private mit domain if the person  has permission for that data"
    #sentence = "MIT can give records to FBI to investigate crimes"
    #sentence = "MIT can give FBI records for criminal investigations"
    #sentence = "police may search people's homes if police have people's permission"
    sentence = "tsa can transfer data to the fbi if the data is associated with  terrorism"
    #sentence = "a service provider may not use phone records to deny service to a customer"
    #sentence = "anyone can access data in the possession of the state of  massachusetts"
    
    #domain = "http://people.csail.mit.edu/oshani/ontologies/university.n3"
    domain = "http://people.csail.mit.edu/oshani/ontologies/federal.n3"
    #domain = "http://people.csail.mit.edu/oshani/ontologies/state.n3"
    
    dict = parseNL(name, sentence)
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
    
