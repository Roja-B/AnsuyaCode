#!/usr/local/bin/python

# This program reads data collected from parenting.com and enters it in MongoDB database called Parenting. 

# Author:Ansuya
# April 2012

import re
import urllib
import pickle
import sys
import os
from pymongo import Connection

sys.setrecursionlimit(100000)

connection = Connection()
parentingdb = connection.Parenting
threads = parentingdb.threads
user=parentingdb.user
posts=parentingdb.posts
i=0

def parse():
    f=open("/home/ansuya/Parenting.txt","r")
    for line in f:
        if (line[:8]=="THREAD_T"):
            threadTitle=line.split(': ')[1].strip()
        if(line[:8]=="THREAD_I"):
            threadId=line.split(': ')[1].strip()
        elif(line[0]=="V"):
            views=line.split(': ')[1].strip()
        elif(line[0]=="M"):
            userId=re.findall("user_id=([^ ]+)",line).pop()
            postId=re.findall("post_id=([^ ]+)",line).pop()
            date=re.findall("([^ ]+)&nbsp;",line).pop()
            time=re.findall("&nbsp;\\s([^#]+)",line).pop().strip()
            orderInThread=re.findall("#([^ ]+)",line).pop()
            userName=re.findall("#[^ ]+(.+)View Profile",line).pop().strip()
            joinDate=re.findall("Join Date  (.+)Posts",line).pop().strip()
            nposts=re.findall("Posts  ([^ ]+)",line).pop().strip()
            postTitle=re.findall("postTitle=(.*)",line).pop().strip()
        elif(line[:4]=="TEXT"):
            text=re.findall("(.+)",line.split(': ')[1]).pop().strip()
        elif(line[0]=="Q"):
            quotePostId=line.split(': ')[1].strip()
            database(threadTitle,threadId,views,userId,postId,date,time,orderInThread,userName,joinDate,nposts,postTitle,text,quotePostId)
    f.close()
            
def database(threadTitle,threadId,views,userId,postId,date,time,orderInThread,userName,joinDate,nposts,postTitle,text,quotePostId):
    global threads
    global user
    global posts
    global i
    log = open("mongoError.log","a")
    new_record1 = [{"threadId" : threadId, "views": views, "threadTitle":threadTitle}]
    threads.insert(new_record1)
    new_record2 = [{"userName" : userName, "userId" : userId, "posts": nposts, "joinDate": joinDate}]
    user.insert(new_record2)
    new_record3 = [{"time" : time, "date" : date, "threadId" : threadId, "orderInthread" : orderInThread, "text": text, "quotePostId" : quotePostId, "postTitle" : postTitle, "userId" : userId}]
    posts.insert(new_record3)
    log.close()
    i=i+1
    print i
    
parse()
print "Total entries processed", i
