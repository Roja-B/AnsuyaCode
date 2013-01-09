#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re
import urllib
import pickle
import sys

sys.setrecursionlimit(3950)
base_url="http://www.mothering.com"

def initialParse():
    url="http://www.mothering.com/community/search.php?search=vaccination&currenttab=Thread&start=0"
    f=open("MotheringSearch.txt","w")
    f.close()
    count=0
    thread_urls=[]
    parseNext(url,count,thread_urls)
    ##print thread_urls
    ##pickle.dump(thread_urls,f)
    ##f.close()

def parseNext(current_url,count,thread_urls):
    print count
    url=urllib.urlopen(current_url).read()
    for m in re.findall("<a href=\"(.+?)\" class=\"title\" >",url):
        thread=base_url+m
        f=open("MotheringSearch.txt","a+")
        f.write(thread)
        f.write("\n")
        f.close()
        thread_urls.append(thread)
    ##not_next=re.search("<span class=\"nxtprv\">Next &raquo;</span>",url)
    ##if(not_next==None):
    ##    l=re.search("(?<=<li>)<a[^<>]*?class=\"tooltip\"[^<>]*?>Next &raquo;</a>",url)
    ##    rel_next_url=re.search("(?<=href=\").*?(?=\")",l.group())
    ##    print l.group()
    ##    next_url=base_url+rel_next_url.group()
    ##    print next_url
    ##    count=count+1
    ##    parseNext(next_url,count)
    ##else:
    ##    print not_next.group()  
    if(count<=39420):
        count=count+10
        next_url="http://www.mothering.com/community/search.php?search=vaccination&currenttab=Thread&start={0}".format(count)
        parseNext(next_url,count,thread_urls)
    else:
        return thread_urls
	    
initialParse()                  
    
