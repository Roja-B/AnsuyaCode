#!urs/local/bin/python
#-*- coding: utf-8 -*
from __future__ import with_statement
from urlparse import urlparse 
import re
import urllib
import sys
import os

sys.setrecursionlimit(100000)

def getDomain(url, tlds):
    try:
        
        urlElements = urlparse(url)[1].split('.')
        # urlElements = ["abcde","co","uk"]

        for i in range(-len(urlElements),0):
            lastIElements = urlElements[i:]
            #    i=-3: ["abcde","co","uk"]
            #    i=-2: ["co","uk"]
            #    i=-1: ["uk"] etc

            candidate = ".".join(lastIElements) # abcde.co.uk, co.uk, uk
            wildcardCandidate = ".".join(["*"]+lastIElements[1:]) # *.co.uk, *.uk, *
            exceptionCandidate = "!"+candidate

            # match tlds: 
            if (exceptionCandidate in tlds):
                return ".".join(urlElements[i:]) 
            if (candidate in tlds or wildcardCandidate in tlds):
                return ".".join(urlElements[i-1:])
                # returns "abcde.co.uk"
    except (ValueError):
        pass         
USER_IDS=[]
LINKS=[]
THREAD_IDS=[]
def parse(f,infile):
    # load tlds, ignore comments and empty lines:
    with open("effective_tld_names.txt") as tldFile:
        tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]   
    user_ids=[]
    posts=[]
    s=1
    for line in f:
        ##print line
        i=re.search("(?s)(?<=user_id=).+?(?=\\s)",line)
        if(i!=None):
            user_ids.append(i.group())
            ##print post_ids
        t=line[ :4]
        if(t=='TEXT'):
            s=0
            posts.append(line)
            ##print posts
        if(s==0):
            break
    user_ids.reverse()
    posts.reverse()
    while(user_ids):
        links=re.findall("http://.+?\\s|https://.+?\\s",posts.pop())
        links.reverse()
        ##print "POST_ID: ",post_ids.pop()
        if(links):
            thread_id=re.search("(?<=MotheringThread).+?(?=.txt)",infile).group()
            THREAD_IDS.append(thread_id)
            USER_IDS.append("\nUSER_ID: ")
            USER_IDS.append(user_ids.pop())
            ##print "LINKS: "
            LINKS.append("\nLINKS: ")
            while(links):
                ##print links.pop()
                domain=getDomain(links.pop(),tlds)
                LINKS.append(str(domain))
        else:
            user_ids.pop()

path = 'Vaccination_Data/motheringsite1/'
listing = os.listdir(path)
counting=0
for infile in listing:
    counting=counting+1
    f=open('Vaccination_Data/motheringsite1/'+infile,"r")
    parse(f,infile)
    f.close()
print counting           
##print POST_IDS
##print LINKS
USER_IDS.reverse()
LINKS.reverse()
THREAD_IDS.reverse()
print len(THREAD_IDS)
print len(USER_IDS)/2
f=open("UserFirstLinksMothering.txt","w")
while(USER_IDS):
    f.write("\nTHREAD_ID: ")
    f.write(THREAD_IDS.pop())    
    f.write(USER_IDS.pop())
    f.write(USER_IDS.pop())
    l=0
    while(l!=2 and LINKS):
            item=LINKS.pop()
            if(item=='\nLINKS: '):
                l=l+1
                ##print l
            if(l==2):
                LINKS.append(item)
            else:
                f.write(item)
                f.write(' ')
print USER_IDS
print LINKS                   
f.close()
        
    
