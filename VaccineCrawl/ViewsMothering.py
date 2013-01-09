#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re
import urllib
import pickle
##import BeautifulSoup

base_url="http://www.mothering.com"

def initialParse():
    URL="http://www.mothering.com/community/f/47/vaccinations/"
    url=urllib.urlopen(URL).read()
    f=open("ViewsMothering.txt","w")
    f.close()
    forum_urls=[]
    for m in re.findall("(?s)<td class=\"forum-col \">.*?<h3>.*?<a.*?href=\"(.*?)\"",url):
        forum=base_url+m
        forum_urls.append(forum)
    forum_urls.pop()
    for m in re.findall("(?s)<span class=\"forum-bullet\">&#8250;</span>.*?<a href=\"(.*?)\"",url):
        forum=base_url+m
        forum_urls.append(forum)
    forum_urls.append(URL)
    print len(forum_urls),"\n"
    count=0
    for forum_url in forum_urls:
        extractViewsNext(forum_url,count)
        

def extractViewsNext(curr_url,count):
    count=count+1
    print count
    ##print curr_url
    url=urllib.urlopen(curr_url).read()
    thread_id=re.findall("data-thread-id=\"(.+?)\"",url)
    thread_id.reverse()
    ##print thread_id
    views=re.findall("<td class=\"narrow-col\">([^\s<>]+?)</td>",url)
    views.reverse()
    ##print views
    f=open("ViewsMothering.txt","a+")
    for thread,view in zip(thread_id,views):
        f.write("THREAD_ID: ")
        ##print thread
        f.write(thread)
        f.write("\n")
        f.write("VIEWS: ")
        ##print view
        f.write(view)
        f.write("\n")
    f.close()
    l=re.search("(?<=<li>)<a[^<>]*?class=\"tooltip\"[^<>]*?>Next &raquo;</a>",url)    
    if(l!=None):
        rel_next_url=re.search("(?<=href=\").*?(?=\")",l.group())
        next_url=base_url+rel_next_url.group()
        extractViewsNext(next_url,count)
    else:
        return None
    
initialParse()
                         
    
