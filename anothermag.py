#!/urs/local/bin/python
#-*- coding: utf-8 -*-
import urllib
from xml.dom.minidom import parseString
import sys
import re

def openURL():
    URL=urllib.urlopen("http://www.anothermag.com/reader/1").read()
    return URL
    
def extract():
    page=openURL()
    f=open("anothermag.txt","w+")
    for m in re.finditer("(?#extract all data between li tags)(?s)(?<=(<li class=\"blog-entry\">)).+?(?=\\1|<div id=\"pager\">)",page):
        entry=0
        ##print "BLOG ENTRY-----> \n"
        f.write("\nBLOG ENTRY-----> \n")
        for k in re.finditer("(?#all text after any tag, including the tag)(?s)<(?=[^(!--)]).+?>.*?(?=<)",m.group()):
                ##print"1111: ", k.group(),"\n"
                i=re.search("(?#image tag)(?s)(?<=src=\").+?.jpg(?=\")",k.group())
                if(i!=None):
                    ##print "3333: ",i.group()
                    if(entry==0):
                        src="www.anothermag.com"+i.group()
                        ##print "\nIMAGE_URL: ",src
                        f.write("\nIMAGE_URL: ")
                        f.write(src)
                        f.write("\n")
                        entry=entry+1
                else:
                    entry=0
                l=re.search("(?#text only)(?s)(?<=>).*",k.group())
                n=re.search("(?s)(<style.*)|(<script.*)",k.group())
                if(n==None):
                    ##print l.group() 
                    f.write(l.group().strip())
                    f.write("\n") 
    f.close()      
extract()
