from pymongo import Connection
from pymongo import errors
from django.utils.encoding import smart_str, smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta
import re
from math import sqrt, log10
from collections import Counter, defaultdict
import sys
sys.setrecursionlimit(1000000)

def topicusers(coms, full_user_com):
    global tt, posts
    coms=sorted(coms)
    full_user_com_topics=[]
    c=0 
    for item in full_user_com:
        user=item[0]
        com=item[1]
        t=[]
        for record in posts.find({"userId":user},timeout=False):
            threadId=smart_str(record["threadId"])
            for entry in tt.find({"threadId":threadId},timeout=False):
                if float(smart_str(entry["maxProportion"])) >= 0.3 :
                    t.extend(list(entry["topics"]))
            c+=1
            print c
        t=list(set(t))
        full_user_com_topics.append((user,com,t))      
    
    print "Users", len(full_user_com_topics)
    
    topics=["0","1","2","3","4","5","6","7","8","9"]
    topic_count_all=Counter()
    topic_count_coms=[]
    for community in coms:
        topic_count=Counter()
        for topic in topics:
            i=0
            while(i<len(full_user_com_topics)):
                if topic in full_user_com_topics[i][2] and community==full_user_com_topics[i][1]:
                    topic_count[topic]+=1
                i+=1
        topic_count=dict(topic_count)
        
        for k,value in sorted(topic_count.items(), key=lambda x: x[1], reverse=True):
            max_topic_count=value
            break
        topic_count_coms.append((community,topic_count, max_topic_count))
    
    for topic in topics:
        i=0
        while(i<len(full_user_com_topics)):
            if topic in full_user_com_topics[i][2]:
                topic_count_all[topic]+=1  
            i+=1  
    topic_count_all=dict(topic_count_all)    
    for k, value in sorted(topic_count_all.items(), key=lambda x: x[1], reverse=True): #sorting by value
        maxtopicfreqcorpus=value
        break
    print len(topic_count_coms), len(topic_count_all)
    #print topic_count_all  
    g=open("/media/netdisk/ansuya/cafemomwork/R/community_topics.csv","w")#data3/cafemomR/top5community_topics.txt","w")
    g.write("communities,Religion,Love and Fun,Day to Day,Vaccination,Family,Birth and Babies,Food,Money and Work,Govt.,Autism\n")
    for c in topic_count_coms:
        #g=open("/media/data3/cafemomR/topic_community{0}.txt".format(c[0]),"w") #/media/netdisk/ansuya/cafemomwork/R/topic_community{0}.txt".format(c[0]),"w")
        #print "For community ", c[0]
        #g.write("community")
        g.write("Com_")
        g.write(c[0])
        g.write(",")
        e=0
        for topic in topics:
            e+=1
            #print "Topic ", topic, "-> ", (float(c[1][topic])/float(c[2]))-(float(topic_count_all[topic])/float(maxtopicfreqcorpus)) 
            g.write(str((float(c[1][topic])/float(c[2]))-(float(topic_count_all[topic])/float(maxtopicfreqcorpus))))
            if e!=10:
                g.write(",")
        g.write("\n")
    g.close()         
    
        
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
tt=Cafemomdb.threadtopic1
log = open("mongoError.log","a")
f=open("/media/data3/cafemomR/results_firstCut.txt","r")#/media/netdisk/ansuya/cafemomwork/cafemom_usersCom.txt","r")
user_com=[]
coms=["4","5","7","8"]
main_coms=["0","1","2","3","6"]
full_user_com=[]
l=0
for line in f:
    user=line.split(" ")[0]
    c=line.split(" ")[1].split("\n")[0]
    if c in coms:
        user_com.append((user,c))
    if c not in main_coms:
        full_user_com.append((user,c)) 
        l+=1   
f.close()
coms_sub={"0":["6"],"1":["1","2","4","5","7","10","13","14","20","21"],"2":["0","1","2","3","4"],"3":["0","1","2", "4","5","7","11","23"],"6":["0","1","2","3","5"]}
for com in main_coms:
    f=open("/media/data3/cafemomR/results_com{0}.txt".format(com),"r")
    sub_coms=coms_sub[com]
    for line in f:
        user=line.split(" ")[0]
        c=line.split(" ")[1].split("\n")[0]
        if c in sub_coms:
            user_com.append((user,com+"_sub_"+c))
            coms.append(com+"_sub_"+c)
        full_user_com.append((user,com+"_sub_"+c))
        l+=1
    f.close()
coms=list(set(coms))
print "Users",len(full_user_com),l, "Users in the big communities", len(user_com)
print len(coms)

topicusers(coms,full_user_com)
log.close()
