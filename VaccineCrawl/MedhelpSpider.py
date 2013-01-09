#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re
import urllib
import pickle

base_url="http://www.medhelp.org"
forum_page_no=1
f=open("/home/ansuya/MedhelpData/MedhelpHtml0.txt","a")
def extractpage(URL,f):
    global forum_page_no
    global base_url
    page=urllib.urlopen(URL).read()
    f.write("\n****medhelp site****html content download****\n")
    f.write(page)
    thread_urls=re.findall("<div class=\'fonts_resizable_subject subject_title \'>\\s+?<a href=\"([^<>]+?)\">",page)
    g=open("/home/ansuya/MedhelpData/MedhelpThreadLinks.txt","a")
    for thread_url in thread_urls:
        thread_url=base_url+thread_url
        g.write(thread_url)
        g.write("\n")
    g.close()
    next_page=re.findall("(?m)<a href=\"([^<>]+?)\"\\sclass=\"msg_next_page\">",page)
    print next_page
    if(next_page):
        forum_page_no+=1
        #print forum_page_no
        next_pg=str(base_url+next_page.pop())
        #print next_pg
        extractpage(next_pg,f)
    else:
        print "Forum pages end", forum_page_no
    f.close()
    
extractpage("http://www.medhelp.org/forums/Immunization--Vaccine-/show/156",f)
