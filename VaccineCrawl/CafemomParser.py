#!/usr/local/bin/python

# This program reads and parses Html from cafemom.com and enters it in MongoDB database called Cafemom. 

# Author:Ansuya
# April 2012

from pymongo import Connection
import re
import sys
import bson 
sys.setrecursionlimit(100000)
    
def recordinsert(record):
    try:
        global posts,users,threads, enteries
        new_record_threads = [{ "groupId" : record[0], "threadId" : record[1], "title": record[2], "replies" : record[3], "views" : record[4]
        }]
        threads.insert(new_record_threads) 
        new_record_users = [{ "userBadge" : record[7], "userId" : record[8], "userName" : record[9]
        }]
        users.insert(new_record_users)
        new_record_posts = [{ "threadStarter" : record[5], "likes" : record[6], "threadId" : record[1], "userId" : record[8], "date" : record[10], "time" : record[11], "text" : record[12], "quote" : record[13], "postId" : record[14]
        }]
        posts.insert(new_record_posts)
        enteries+=1
        print "Entry", enteries
    except (bson.errors.InvalidStringData, IndexError):
        pass

def readUrls():
    global count
    textfile=1
    while(textfile!=5):
        f=open("/media/netdisk/cafemomsite/CafemomThreadHtml{0}.txt".format(textfile),"r")
        page=''
        for line in f:
            line=line.strip()
            #print line
            if(line!= "****cafemom site****html content download****" or line!="</html>"):
                page=page+line
            if(line=="</html>"):
                group_thread_id=re.findall("(/group/(\\d+)/forums/read/(\\d+)/.+?<!DOCTYPE)",page)
                if(group_thread_id):
	                count=count+1
	                print "THREAD PAGE COUNT", count
	                if(re.search("next=",group_thread_id[0][0])):
	                    text(page,group_thread_id[0][1],group_thread_id[0][2],0)
	                else:
	                    text(page,group_thread_id[0][1],group_thread_id[0][2],1)
                page=''
        f.close()
        textfile+=1
    print "THREAD PAGE COUNT", count
      
def text(page,group_id,thread_id,startpage):
    global enteries
    title=''
    thread_title=re.search("(?<=<h1 class=\"post\">)(.+?)(?=</h1>)",page)
    if(thread_title):
        title=thread_title.group()
    replies=re.findall("<span class=\"iconCommunity iconReply\"></span>(.+?)Replies",page)   
    views=re.findall("<li class=\"views spaceBottom5\"><span>(.+?)Total Views",page)
    
    if(startpage==1):
        record=[]
        start_post=re.search("<div class=\"aComment clearfix\">.+?<div class=\"clearfix bgAquamarine darkGrey small\">.*?<",page)
        if(start_post):
            record.append(group_id)
            record.append(thread_id)
            record.append(title)
            startpost=start_post.group()
            if(replies):
                record.append(replies[0].strip())
            else:
                record.append('')
            if(views):
                record.append(views[0].strip())
            else:
                record.append('')
            record.append(startpage)
            text11(startpost,record,group_id,thread_id)
            replyposts=re.findall("(<a name=\"post(.+?)\">.+?<ul class=\"blockList\">.*?<)",page)
            for post in replyposts:
                record=[]
                record.append(group_id)
                record.append(thread_id)
                record.append(title)
                if(replies):
                    record.append(replies[0].strip())
                else:
                    record.append('')
                if(views):
                    record.append(views[0].strip())
                else:
                    record.append('')
                record.append(0)
                text12(post[0],record,group_id,thread_id,post[1])
    elif(startpage==0):
        replyposts=re.findall("(<a name=\"post(.+?)\">.+?<ul class=\"blockList\">.*?<)",page)
        for post in replyposts:
            record=[]
            record.append(group_id)
            record.append(thread_id)
            record.append(title)
            if(replies):
                record.append(replies[0].strip())
            else:
                record.append('')
            if(views):
                record.append(views[0].strip())
            else:
                record.append('')
            record.append(startpage)
            text12(post[0],record,group_id,thread_id,post[1])       
          
def text11(post,record,group_id,thread_id):
    stay1=0
    stay2=0 
    text=''
    
    likes=re.findall("<span class=\"iconCommunity iconLiked\"></span>.*?(\\d+?) mom liked this",post)
    if(likes):
        record.append(likes[0])
    else:
	    record.append('0')
	   
    user_title=re.findall("class=\"rankBadge.+?\">(.+?)<",post)
    if(user_title):
        record.append(user_title[0].strip())
    else:
        record.append('')
	    	    
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            #print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            user_info=re.findall("<ul onclick=\"ScreenNameDD.showMenu\(this, \{user_id:'(\\d+)', screen_name:'(.+?)', title:''\}\);\"",m.group())
            if(user_info):
                record.append(user_info[0][0])
                record.append(user_info[0][1])
            date_time=re.search("onclick=\"this.blur\(\);return\(false\);\">",m.group())
            if(date_time or stay1==1):
                stay1=1
                end=re.search("<div class=\"spaceBottom5\">",m.group())
                date_time_tag=re.findall("</ul>on(.+?)at(.+)",m.group())
                if(date_time_tag):
                    record.append(date_time_tag[0][0].strip())
                    record.append(date_time_tag[0][1].strip())
                elif(end):
                    stay1=0
            text_start=re.search("<div class=\"boardPostBody\"",m.group())
            if(text_start or stay2==1):
                stay2=1
                end=re.search("<div class=\"clearfix bgAquamarine darkGrey small\">",m.group())
                if(end==None):
                    if(n==None):
                        text=text+l.group().strip().replace("\n"," ")+' '   
                else:
                    record.append(text.strip())
                    record.append('')
                    stay2=0
    
    print group_id, thread_id            
    post_id=re.findall("&quote_post=(\\d+?)\" class=\"standardBtn btnGreen suffix5\">Quote</a>",post)
    if(post_id):
        record.append(post_id[0]) 
    else:
        record.append('')
    print "recordlen", len(record) #, record
    recordinsert(record)
             
def text12(post,record,group_id,thread_id,post_id):
    stay2=0
    stay21=0
    text=''
    quote=''
    likes=re.findall("<span class=\"iconCommunity iconLiked\"></span>.*?(\\d+?) mom liked this",post)
    if(likes):
        record.append(likes[0])
    else:
        record.append('0')
        
    user_title=re.findall("class=\"rankBadge.+?\">(.+?)</a>on(.+?)at(.+?)<",post)
    if(user_title):
        record.append(user_title[0][0].strip())
    else:
        record.append('') 
		    		      
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            #print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            user_info=re.findall("<ul onclick=\"ScreenNameDD.showMenu\(this, \{user_id:'(\\d+)', screen_name:'(.+)', title:''\}\);\"",m.group())
            if(user_info):
                record.append(user_info[0][0])
                record.append(user_info[0][1])
                if(user_title):
                    record.append(user_title[0][1].strip())
                    record.append(user_title[0][2].strip())
                else:
                    date_time=re.findall("</ul>on(.+?)at(.+?)<",post)
                    if(date_time):
                        record.append(date_time[0][0].strip())
                        record.append(date_time[0][1].strip())
                            
            text_start=re.search("<div class=\"clearfix forumReplyBody\"",m.group())
            if(text_start or stay2==1):
                stay2=1
                end=re.search("<ul class=\"blockList\">",m.group())
                quote_start=re.search("<blockquote class=\"quotedText\">",m.group())
                if(quote_start or stay21==1):
                    stay21=1
                    quote_end=re.search("</blockquote>",m.group())
                    if(quote_end==None):
                        if(n==None):
                            quote=quote+l.group().strip().replace("\n"," ")+' '
                    else:
                        stay21=0 
                if(end==None and stay21==0):
                    if(n==None):
                        text=text+l.group().strip().replace("\n"," ")+' '    
                elif(end!=None):
                    record.append(text.strip())
                    record.append(quote.strip())
                    stay2=0   
    
    print group_id, thread_id 
    record.append(post_id)
    print "recordlen", len(record) #, record
    recordinsert(record)
           
connection = Connection()
cafemomdb = connection.Cafemom
posts = cafemomdb.posts
users=cafemomdb.users
threads=cafemomdb.threads
log = open("mongoError.log","a")
enteries=0
count=0
readUrls()
print "Total enteries processed", enteries
log.close()
