#!/usr/bin/env /mit/6.863/arch/i386_deb40/bin/python-nlp 

import cgi
from StringIO import StringIO
import sys

def send_header(outfile, keyword, value):
        outfile.write("%s: %s\r\n" % (keyword,value))

def end_headers(outfile):
        outfile.write("\r\n")

def main():
        
        
        ctype = 'text/rdf+n3'
        outfile = sys.stdout
        sys.stdout = StringIO()

        form = cgi.FieldStorage()

        """
        name = "MITProxCardDataPolicy"
        sentence = "MIT can use prox card data for criminal investigation"
        domain = "../data/university.n3"
        """
        
        name = form["name"].value
        sentence = form["sentence"].value
        domain =  form["domain"].value
        
        dict = parseNL(name, sentence)
        s = constructPolicy(dict, domain)
        
        if s == "Please check the policy sentence!":
            ctype = "text/plain"

        send_header(outfile, "Content-type",ctype)

        s = s.encode('utf_8')
        length = str(len(s))

        send_header(outfile, "Content-Length", length)
        end_headers(outfile)
        outfile.write(s)
        sys.stdout = outfile

if __name__ == '__main__':
    
    import sys
    sys.path.append("../PolicyInterpreter/")
    sys.path.append("../featureparse")
    sys.path.append("../RDFGenerator")

    from generate import *
    from policyParser import *
    from condition import *

    main()
