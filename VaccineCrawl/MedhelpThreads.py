#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re
import urllib
import pickle

base_url="http://www.medhelp.org"
thread_no=0
def extractpage():
    global thread_no
    global base_url
    f=open("/home/ansuya/MedhelpData/MedhelpThreadLinks.txt","r")
    for line in f:
        if(line!="\n"):
            thread_no+=1
            print "THREAD",thread_no
            g=open("/home/ansuya/MedhelpData/MedhelpHtml1.txt","a")
            page=urllib.urlopen(line).read()
            prev_page_in_thread=re.search("(?<=<a href=\")(.+?)(?=\" class=\"msg_previous_page\">)",page)
            if(prev_page_in_thread):
                insidepage=1
                print insidepage
                pagesinthread=[]
                urlpagesinthread=[]
                pagesinthread.append(page)
                urlpagesinthread.append(line)
                while(prev_page_in_thread!=None):
                    urlpagesinthread.append(base_url+prev_page_in_thread.group())
                    prev_page=urllib.urlopen(base_url+prev_page_in_thread.group()).read()
                    pagesinthread.append(prev_page)
                    insidepage+=1
                    print insidepage
                    prev_page_in_thread=re.search("(?<=<a href=\")(.+?)(?=\" class=\"msg_previous_page\">)",prev_page)
                pagesinthread.reverse()
                urlpagesinthread.reverse()
                for pg,link in zip(pagesinthread,urlpagesinthread):
                    g.write("\n****medhelp site****html content download****\n")
                    g.write(link)
                    g.write("\n")
                    g.write(pg) 
            else:   
                g.write("\n****medhelp site****html content download****\n")
                g.write(line)
                g.write("\n")
                g.write(page)
        else:
            print "End of thread list",thread_no
    g.close()
    f.close()
    
extractpage()
