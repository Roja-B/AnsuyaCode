#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re
import urllib
import pickle
import os

base_url="http://forums.parenting.com/"

def initialParse():
    URL="http://forums.parenting.com/forumdisplay.php?164-Vaccines"
    url=urllib.urlopen(URL).read()
    f=open("Parenting.txt","w")
    f.close()
    threads=re.findall("<a class=\"title\" href=\"(.+?)\" id=\"thread_title_(.\\d+?)\">(.+?)</a>",url)
    views=re.findall("<li>Views: (.+?)</li>",url)
    ##print len(threads)
    count=1
    for thread,v in zip(threads,views):
        print "THREAD", count
        f=open("Parenting.txt","a+")
        if(os.stat("Parenting.txt")[6]==0):
            f.write("THREAD_TITLE: ")
        else:
            f.write("\nTHREAD_TITLE: ")
        f.write(thread[2])
        f.write("\n")
        link=base_url+thread[0]
        f.write("THREAD_URL: ")
        f.write(link)
        f.write("\n")
        f.write("THREAD_ID: ")
        f.write(thread[1])
        f.write("\n")
        f.write("VIEWS: ")
        f.write(v)
        f.close()
        parsePage(link)
        count=count+1
    
def parsePage(url):
    thread=urllib.urlopen(url).read()
    posts=re.findall("(?s)(<li class=\"postbit.+?id=\"post_(\\d+?)\">.+?(?= Reply With Quote</a>))",thread)
    ##print "NO OF POSTS", len(posts)
    ##print posts
    count=0
    usr_ids=re.findall("(?s)<a class=\"username offline popupctrl\" href=\".+?\\?(.+?)-.+?</ul>",thread)
    ##print usr_ids
    ##print "NO OF USR IDS", len(usr_ids)
    for post,usr_id in zip(posts,usr_ids):
       count=count+1
       print count
       f=open("Parenting.txt","a+")
       f.write("\nMETA-DATA: ")
       f.write("user_id=")
       ##print usr_id
       f.write(usr_id)
       f.write(" post_id=")
       ##print post[1]
       f.write(post[1])
       f.close()
       text(post[0],post[1],usr_id)
    next=re.findall("<a rel=\"next\" href=\"(.+?)\"",thread)
    if(next):
        next_url=base_url+next.pop()
        ##print next_url
        parsePage(next_url)
    else:
        print"END"
    
    
def text(block,post_id,usr_id):
    f=open("Parenting.txt","a+")
    enter=1
    remain1=0
    remain2=0
    remain3=0
    cnt=1
    qPId=""
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",block):
        if(m!=None):
            postTitle=re.search("<h2 class=\"posttitle icon\">",m.group())
            if(postTitle or remain1==1):
                #print m.group()
                remain1=1
                if(cnt==2):
                    postTitle1=re.findall("Default\" />(.*)",m.group())   
                if(cnt==3):
                    remain1=0
                cnt=cnt+1
            quote=re.search("<div class=\"quote_container\">",m.group())
            if(quote or remain2==1):
                remain2=1
                quotePostId=re.findall("<a href=\"(.+)\" rel=\"nofollow\">",m.group())
                if(quotePostId):
                    qPId=quotePostId.pop().split('#')[1][4:]
                if(re.search("blockquote",m.group())):
                    remain2=0
            lastedited=re.search("<blockquote class=\"postcontent lastedited\">",m.group())
            if(lastedited):
                 remain3=1 
            ##print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            ##print l.group()
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            if(re.search("<div class=\"content\">",m.group())):
                f.write(" postTitle=")
                if(postTitle1):
                    postTitle1=postTitle1.pop().strip()
                    f.write(str(postTitle1))
                f.write("\nTEXT: ")
            if(n==None and enter==1 and remain1==0 and remain2==0 and remain3==0):
                ##print"2222: ", l.group()
                f.write(l.group().strip().replace('\n',' '))
                f.write(' ')
    f.write("\nQUOTE: ")
    f.write(qPId)        
    f.close()
    
initialParse()   
