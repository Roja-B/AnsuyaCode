from pymongo import Connection
from pymongo import errors
from django.utils.encoding import smart_str, smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta
import re
import os,sys
sys.setrecursionlimit(1500000)
def topictop3threads():
    countthreads = 0
    countposts=0
    lcount=0
    c=0
    h=open('/media/netdisk/ansuya/mallet-2.0.7/cafemomthread1doctopics','r')
    for line in h:
        if lcount>0 :
            l=line.split('\t')
            #print l
            threadId=l[1].split('/')[6].split('.')[0]
            s=0
            if l[2]=="3" :    s=1
            elif l[4]=="3" :   s=1 
            elif l[6]=="3" :  s=1
            if s==1:
                countthreads+=1
                print "Thread", countthreads
                g=open("/media/netdisk/threadtop3topic3full.txt","a")
                g.write(threadId)
                g.write("\n")
                f=open("/media/netdisk/Topic3top3full/data/{0}.txt".format(threadId),"w")
                for post in posts.find({"threadId" : threadId}, timeout=False):
                    vax=re.search("(?i)(\\s|\\W)va[x(ccin)]",smart_str(post["text"]))
                    if vax :
                        c+=1
                        print "Number of posts with vaccine word in it ", c
                    f.write(smart_str(post["text"]))
                    f.write("\n")
                    countposts+=1
                print countposts
                f.close()
            s=0
        lcount+=1
        
    g.close()
    h.close()
    print "Threads", countthreads, "Posts", countposts    
    
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
tt=Cafemomdb.threadtopic1
log = open("mongoError.log","a")
i=0
while i<=9:
    os.makedirs("/media/netdisk/ansuya/topic{0}".format(i))
    os.makedirs("/media/netdisk/ansuya/topic{0}/data/".format(i))
    count=0
    for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
        threadId=smart_str(entry["threadId"])
        topics=list(entry["topics"])
        if str(i) in topics:
            f=open("/media/netdisk/ansuya/topic{0}/data/{1}.txt".format(i,threadId),"w")
            for post in posts.find({"threadId" : threadId}, timeout=False):
                f.write(smart_str(post["text"]))
                f.write("\n")
            count+=1
            print count
            f.close()
    print "No. of threads with max Prop >0.3 and have topic "+str(i)+" most associated with it", count
    i+=1
   
