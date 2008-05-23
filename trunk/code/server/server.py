#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp

def main():
    
    name = "MITProxCardDataPolicy"
    
    #sentence = "MIT can use prox card data for criminal investigations"
    #sentence = "police may search people's homes if police have people's permission"
    sentence = "a person may access data on the private mit domain if the person  has permission for that data"
    #sentence = "a service provider may not use phone records to deny service to a customer"
    #sentence = "tsa can transfer data to the fbi if the data is associated with  terrorism"
    #sentence = "anyone can access data in the possession of the state of  massachusetts"
    #sentence = "MIT can give records to FBI to investigate crimes"
    #sentence = "MIT can give FBI records for criminal investigations"
    
    domain = "../data/university.n3"
    #domain = "../data/federal.n3"
    #domain = "../data/state.n3"
    
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
    
