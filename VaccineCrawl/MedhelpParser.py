#!/usr/local/bin/python

# This program reads parses Html from medhelp.org and enters it in MongoDB database called Medhelp. 

# Author:Ansuya
# April 2012

from pymongo import Connection
import re
import urllib
import sys
import os

sys.setrecursionlimit(100000)
    
def record1(record):
    global posts
    new_record = [{
    "threadId" : record[0],
    "postId" : record[1],
    "userId" : record[2],
    "userName" : record[3],
    "date" : record[4],
    "text" : record[5],
    "title" : record[6],
    "tags" : record[7]
    }]
    posts.insert(new_record)

def record2(record):
    global posts
    new_record = [{
    "threadId" : record[0],
    "postId" : record[1],
    "userId" : record[2],
    "userName" : record[3],
    "date" : record[4],
    "text" : record[5],
    "title" : record[6],
    "replyTo" : record[7]
    }]
    posts.insert(new_record) 

def readUrls():
    f=open("/home/ansuya/MedhelpData/MedhelpHtml1.txt","r")
    count=0
    page=''
    for line in f:
	    line=line.strip()
	    if(line!= "****medhelp site****html content download****" or line!="</html>"):
	        page=page+line
	    if(line=="</html>"):
	        thread_id=re.search("(?<=/show/)(.+)(?=<!DOCTYPE)",page).group()
	        count=count+1
	        print "THREAD COUNT", count
	        text(page,thread_id)
	        page=''
    f.close()
    print "THREAD COUNT", count
      
def text(page,thread_id):
    global enteries
    posts=re.findall("(?s)(<div class=\'user_info\'>.+?<div id=\"post_(.+?)\" class='post_data has_bg_color'>.+?<div class='post_footer float_fix '>.+?<|<div id=\"post_(.+?)\" class='post_data has_bg_color'>.+?<div class='post_footer float_fix has_bg_color'>.+?<)",page)
    #print len(posts)
    order=1
    for post in posts:
        #print post
        record=[]
        test=re.search("<div class=\'user_info\'>",post[0])
        if(order==1 and test==None):
            record.append(thread_id)
            record.append(post[1])
            text12(post[0],record)
        elif(order==1 and test!=None):
            record.append(thread_id)
            record.append(post[1])
            text11(post[0],record)
        else:
            record.append(thread_id)
            record.append(post[2])
            text12(post[0],record)
        order=order+1
        enteries=enteries+1
        print enteries
        #break
          
def text11(post,record):
    global thtitle
    stay1=0
    stay2=0
    stay21=0
    stay3=0
    stay4=0
    text=''
    user_stats=''
    title=''
    tags=[]
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            #print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            titletag=re.search("<h1 class=\"post_question_forum_title fonts_resizable\">",m.group())
            if(titletag or stay1==1):
                stay1=1
                end=re.search("</h1>",m.group())
                if(end==None):
                    if(n==None):
                        title=title+l.group().strip().replace("\n"," ")+' '    
                if(end!=None):
                    stay1=0
                    thtitle=title.strip()
               
            user_first_post=re.search("<div class=\'user_info\'>",m.group())
            if(user_first_post or stay2==1):
                stay2=1
                end=re.search("<div class='subject_comments_number'>",m.group())
                if(end==None):
                    if(n==None):
                        user_stats=re.findall("(<a href=\".+?\" id=\"user_(\\d+?)_\\d+?\">(.+))",m.group())
                        if(user_stats):
                            user_stats=user_stats.pop()
                            userName=user_stats[2]
                            userId=user_stats[1]
                            record.append(userId)
                            record.append(userName)
                        datetag=re.search("<span class=\'separator\'>",m.group())
                        if(datetag or stay21==1):
                            stay21=1
                            date=re.search("(?<=</span>)(.+)",m.group())
                            if(date):
                                record.append(date.group())
                                stay21=0
                elif(end!=None):
                    stay2=0
                    
            texttag=re.search("<div class='KonaBody'>",m.group())
            if(texttag or stay3==1):
                stay3=1
                end=re.search("<div class='post_footer float_fix '>",m.group())
                if(end==None):
                    if(n==None):
                        text=text+l.group().strip().replace("\n"," ")+' '    
                if(end!=None):
                    record.append(text.strip())
                    record.append(thtitle)
                    stay3=0
                    
            tagtag=re.search("<span class='post_question_tags'>",m.group())
            if(tagtag or stay4==1):
                stay4=1
                end=re.search("<div class='post_footer float_fix '>",m.group())
                if(end==None):
                    if(n==None):
                        tag=re.findall("<a href=\"(.+?)\">",m.group())
                        if(tag):
                            tags.extend(tag)
                if(end!=None):
                    stay4=0
    record.append(tags)
    #print record
    print thtitle
    record1(record)
		                    
def text12(post,record):
    global thtitle
    stay1=0
    stay11=0
    stay2=0
    stay3=0
    to=''
    user_stats=''
    text=''
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            ##print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
           
            user_other_post=re.search("<div class=\"question_by\">",m.group())
            if(user_other_post or stay1==1):
                stay1=1
                end=re.search("<div class='post_question_forum_to'>",m.group())
                if(end==None):
                    if(n==None):
                        user_stats=re.findall("(<a href=\".+?\" id=\"user_(\\d+?)_\\d+?\">(.+))",m.group())
                        if(user_stats):
                            user_stats=user_stats.pop()
                            userName=user_stats[2]
                            userId=user_stats[1]
                            record.append(userId)
                            record.append(userName)
                        datetag=re.search("<span class=\"seperator\">",m.group())
                        if(datetag or stay11==1):
                            stay11=1
                            date=re.search("(?<=<div>)(.+)",m.group())
                            if(date):
                                record.append(date.group())
                                stay11=0
                elif(end!=None):
                    stay1=0
                    
            totag=re.search("<div class='post_question_forum_to'>",m.group())
            if(totag or stay2==1):
                stay2=1 
                end=re.search("<div class='frm_post_msg'>",m.group())
                if(end==None):
                    if(n==None):
                        to=to+l.group().strip().replace("\n"," ")+' '  
                elif(end!=None):
                    stay2=0
                    
            texttag=re.search("<div class='KonaBody'>",m.group())
            if(texttag or stay3==1):
                stay3=1
                end=re.search("<div class='post_footer float_fix has_bg_color'>",m.group())
                if(end==None):
                    if(n==None):
                        text=text+l.group().strip().replace("\n"," ")+' '    
                if(end!=None):
                    record.append(text.strip())
                    record.append(thtitle)
                    stay3=0
    if(re.search("<div class='post_question_forum_to'>",post)==None):
        record.append('')
    else:
        record.append(to[3:].strip())
    #print record
    print thtitle
    record2(record) 
        
connection = Connection()
medhelpdb = connection.Medhelp
posts = medhelpdb.posts
log = open("mongoError.log","a")
thtitle=''
enteries=0
readUrls()
print "Total enteries processed", enteries
log.close()
