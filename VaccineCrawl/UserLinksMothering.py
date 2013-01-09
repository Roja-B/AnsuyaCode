#!urs/local/bin/python
#-*- coding: utf-8 -*
import re
import urllib
import sys
import os

sys.setrecursionlimit(100000)
         
USER_IDS=[]
LINKS=[]
def parse(f):
    user_ids=[]
    posts=[]
    for line in f:
        ##print line
        i=re.search("(?s)(?<=user_id=).+?(?=\\s)",line)
        if(i!=None):
            user_ids.append(i.group())
            ##print post_ids
        t=line[ :4]
        if(t=='TEXT'):
            posts.append(line)
            ##print posts
    user_ids.reverse()
    posts.reverse()
    while(user_ids):
        links=re.findall("http://.+?\\s|https://.+?\\s",posts.pop())
        links.reverse()
        ##print "POST_ID: ",post_ids.pop()
        if(links):
            USER_IDS.append("\nUSER_ID: ")
            USER_IDS.append(user_ids.pop())
            ##print "LINKS: "
            LINKS.append("\nLINKS: ")
            while(links):
                ##print links.pop()
                LINKS.append(links.pop())
        else:
            user_ids.pop()

path = 'Vaccination_Data/motheringsite1/'
listing = os.listdir(path)
counting=0
for infile in listing:
    counting=counting+1
    f=open('Vaccination_Data/motheringsite1/'+infile,"r")
    parse(f)
    f.close()
print counting           
##print POST_IDS
##print LINKS
USER_IDS.reverse()
LINKS.reverse()
f=open("UserLinksMothering.txt","w")
while(USER_IDS):
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
print USER_IDS
print LINKS                   
f.close()
        
    
