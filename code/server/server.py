#!/usr/bin/env python
"""server cgi

An attempt to get a cgi interface to Policy Editor

"""
ctype = 'text/rdf+n3'

import cgi

# instead of cgi.FieldStorage, can we use  paste.wsgiwrappers.WSGIRequest(env).params, 
# as documented in
# http://pythonpaste.org/class-paste.wsgiwrappers.WSGIRequest.html and 
# http://pythonpaste.org/class-paste.util.multidict.MultiDict.html
# connecting to cgi using wsgiref would be a first start
# but I would need a wsgi interface
# FieldStorage seems incompatible --- this is a problem
# It seems (although the docs do not say this) that you
# can run
# stdin = environ['wsgi.input']
# 

from StringIO import StringIO



def send_header(outfile, keyword, value):
    """Send a MIME header."""
    outfile.write("%s: %s\r\n" % (keyword, value))

def end_headers(outfile):
    """Send the blank line ending the MIME headers."""
    outfile.write("\r\n")

def main():
    
    import sys
    outfile = sys.stdout
    sys.stdout = StringIO()
    form = cgi.FieldStorage()
    
    name = "MITProxCardDataPolicy"
    sentence = "MIT can use proxy for criminal"
    domain = "data/university.n3"

    dict = parseNL(name, sentence)
    returnString = constructPolicy(dict, domain)
    returnString = returnString.encode('utf_8')
    print "<HTML>"+returnString+"</HTML>"
    
    """
        name = form.getlist('policy_name')
    sentence = form.getlist('policy_sentence')
    domain = form.getlist('domain')

 print ('ran constructPolicy(%s, %s, %s)\n' % (name, sentence, domain))
    print (str(form.keys()) + '\n')
    send_header(outfile, "Content-type", ctype)
    if DEBUG:
        length = str(len(returnString) + len(sys.stdout.getvalue()))
    else:
        length =  str(len(returnString))
    send_header(outfile, "Content-Length", length)
#    print ctype
    end_headers(outfile)
    if DEBUG:
        outfile.write(sys.stdout.getvalue())
    outfile.write(returnString)
    sys.stdout = outfile
    """

if __name__ == '__main__': # What else would it be?
    
    import sys
    
    sys.path.append("PolicyParser/")
    sys.path.append("featureparse")
    sys.path.append("RDFGenerator")

    from pparser import *
    from Condition import *
    from generate import *
    
    main()
