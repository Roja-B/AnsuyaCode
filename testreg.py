import re

def reg():
    f=open("TestHTML.txt","r").read()
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",f):
        if(m!=None):
            print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            if(n==None):
                print"2222: ", l.group()
                
    
reg()
