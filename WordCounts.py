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

def topicthreads():
    global posts
    global tt
    global stopwords
    count=0
    dates=set()
    post_date=[]
    months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
    pId=1
    for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
        threadId=smart_str(entry["threadId"])
        topics=list(entry["topics"])
        if "3" in topics:
            for post in posts.find({"threadId" : threadId}, timeout=False):
                postdate=smart_str(post["date"])
                month= [months[key] for key in months.keys() if postdate[:3] in key]
                try:
                    day=int(postdate[5:7])
                except ValueError:
                    day=int(postdate[5:6])
                year=int(postdate[8:])
                d=date(year,month.pop(),day)
                dates.add(d)
                threadId=smart_str(post["threadId"])
                postId=smart_str(post["postId"])
                text=smart_str(post["text"])
                if(postId==""):
                    postId=pId
                    pId+=1
                post_date.append((threadId,postId,d, text))
                count+=1
            print "post", count, len(post_date)
            
    dates=list(dates)
    oldest_date=min(dates)
    youngest_date=max(dates)
    print "Oldest date", oldest_date
    print "Youngest date", youngest_date

    start=oldest_date
    timeslots=[]
    while start<=youngest_date:
        end=start+relativedelta(months = +6)
        timeslots.append((start,end))
        start=end
    num_timeslots=len(timeslots)
    print num_timeslots, timeslots 
    slots=[]
    i=0
    while i<num_timeslots:
        slots.append([])
        i+=1
    print "Num of slots", len(slots), num_timeslots
    
    postcount=0
    for entry in post_date:
        i=0
        while i<num_timeslots:
            if entry[2]>=timeslots[i][0] and entry[2]< timeslots[i][1]:
                #f=open("/media/netdisk/topic3(<0.3)/threadId_postId_date_slot{0}.txt".format(i),"a")
                #f.write(entry[0])
                #f.write("\t")
                #f.write(str(entry[1]))
                #f.write("\t")
                #f.write(str(entry[2]))
                #f.write("\n")
                postcount+=1
                #print "Post added to file", postcount
                slots[i].append(entry[3])
                #f.close()
            i+=1
    #print "Posts added to file", postcount
    tslot=[]
    totalwordsinslot=[]
    all_tokens=[]
    for slot in slots:
        string=""
        for text in slot:
            string+=text+" "
        tokens=re.findall("\\w{3,}",string.strip())#nltk.word_tokenize(string.strip())
        new_tokens=[]
        for token in tokens:
            token=token.lower()
            #token=token.split(".")[0]
            #token=token.split(",")[0]
            #token=token.split("&")[0]
            if token not in stopwords:
                new_tokens.append(token)
                all_tokens.append(token)
        totalwordsinslot.append(len(new_tokens))
        print "Total number of words in this slot", len(new_tokens)
        wordcount=Counter()
        for word in new_tokens :
            wordcount[word]+=1
        print "Total number of unique unigrams in this slot", len(wordcount)
        tslot.append(wordcount)
    print "Slots", len(tslot), len(totalwordsinslot)
    totalwordsincorpus=len(all_tokens)
    print "Total words in the corpus", totalwordsincorpus
    totalwordcount=Counter()
    for word in all_tokens:
        totalwordcount[word]+=1
   
    print "Total number of unique unigrams in the entire corpus", len(totalwordcount)
    i=0
    totalwords=0
    g=open("/media/netdisk/topic3(<0.3)/top10zscoreperslot3.txt","w")#top10termsperslot.txt","w")
    g.write("word   prob_slot   prob_corpus     zscore\n")
    for slot in tslot:
        words=slot.keys()
        word_zscore=[]
        word_p=[]
        probs=0.0
        #term_prob=[]
        #f=open("/media/netdisk/topic3(<0.3)zscore_slot{0}.txt".format(i),"w")#/tf_slot{0}.txt".format(i),"w")
        for word in words:
            slottermcount=slot[word]
            totaltermcount=totalwordcount[word]
            p=float(totaltermcount)/float(totalwordsincorpus)
            n=float(totalwordsinslot[i])
            x=float(slottermcount)
            zscore=(x-(n*p))/sqrt(n*p*(1-p))
            #probofterm=float(slottermcount)/float(totalwordsinslot[i])
            #f.write(word)
            #f.write("\t")
            #f.write(str(probofterm))#zscore))
            #f.write("\n")
            word_zscore.append((word,zscore))
            word_p.append((word,p))
            probs+=p
            #term_prob.append((word,probofterm))
            totalwords+=1
        #f.close()
        avgp=probs/n
        d=dict(word_zscore)
        e=dict(word_p)
        #d=dict(term_prob)
        sorted_d=sorted(d.items(), key=lambda x: x[1], reverse=True)
        sorted_d=sorted_d[:100]
        g.write("slot ")
        g.write(str(i))
        g.write("\n")
        c=0
        for entry in sorted_d:
            if e[entry[0]] > avgp and c<10:
                c+=1
                g.write(entry[0])
                g.write("\t")
                g.write(str(float(slot[entry[0]])/n))
                g.write("\t")
                g.write(str(float(totalwordcount[entry[0]])/float(totalwordsincorpus)))
                g.write("\t")
                g.write(str(entry[1]))
                g.write("\n")
        i+=1
    g.close()
    print "Total unigrams added to different slots", totalwords
    
def tfidf() :
    global posts
    global tt
    global stopwords
    count=0
    dates=set()
    post_date=[]
    months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
    pId=1
    for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
        threadId=smart_str(entry["threadId"])
        topics=list(entry["topics"])
        if "3" in topics:
            for post in posts.find({"threadId" : threadId}, timeout=False):
                postdate=smart_str(post["date"])
                month= [months[key] for key in months.keys() if postdate[:3] in key]
                try:
                    day=int(postdate[5:7])
                except ValueError:
                    day=int(postdate[5:6])
                year=int(postdate[8:])
                d=date(year,month.pop(),day)
                dates.add(d)
                threadId=smart_str(post["threadId"])
                postId=smart_str(post["postId"])
                text=smart_str(post["text"])
                if(postId==""):
                    postId=pId
                    pId+=1
                post_date.append((threadId,postId,d, text))
                count+=1
            print "post", count, len(post_date)
            
    dates=list(dates)
    oldest_date=min(dates)
    youngest_date=max(dates)
    print "Oldest date", oldest_date
    print "Youngest date", youngest_date

    start=oldest_date
    timeslots=[]
    while start<=youngest_date:
        end=start+relativedelta(months = +3)
        timeslots.append((start,end))
        start=end
    num_timeslots=len(timeslots)
    print num_timeslots, timeslots 
    slots=[]
    i=0
    while i<num_timeslots:
        slots.append([])
        i+=1
    print "Num of slots", len(slots), num_timeslots
    
    postcount=0
    for entry in post_date:
        i=0
        while i<num_timeslots:
            if entry[2]>=timeslots[i][0] and entry[2]< timeslots[i][1]:
                postcount+=1
                slots[i].append(entry[3])# post text added to different time slots
                
            i+=1
    tslot=[]
    for slot in slots:
        string=""
        for text in slot:
            string+=text+" "
        tokens=re.findall("\\w{3,}",string.strip())
        new_tokens=[]
        for token in tokens:
            token=token.lower()
            if token not in stopwords:
                new_tokens.append(token)
        wordcount=Counter()
        for word in new_tokens :
            wordcount[word]+=1
        print "Total number of unique unigrams in this slot", len(wordcount)
        tslot.append(wordcount)
    print "Slots", len(tslot)
    
    slotstermtfidf=[]
    for slot in tslot:
        words=slot.keys()
        wc={}
        for word in words:
            NumOfDocTerm=0 # Number of documents which contain this term
            for slot1 in tslot:
                owords=slot1.keys()
                if word in owords:
                    NumOfDocTerm+=1
            termFreq=slot[word]
            tfIDF= float(termFreq)* log10(num_timeslots/NumOfDocTerm)  
            wc[word]=tfIDF
        slotstermtfidf.append(wc)
    i=0
    g=open("/media/netdisk/topic3(<0.3)/top10tfidfperslot.txt","w")
    g.write("word   tf*idf\n")
    for slot in slotstermtfidf:           
        d=dict(slot)
        sorted_d=sorted(d.items(), key=lambda x: x[1], reverse=True)
        sorted_d=sorted_d[:10]
        g.write("slot ")
        g.write(str(i))
        g.write("\n")
        for entry in sorted_d:
            g.write(entry[0])
            g.write("\t")
            g.write(str(entry[1]))
            g.write("\n")
        i+=1
    g.close()
    
def subcount():
    global posts
    global tt
    global stopwords
    T=0
    while T<=9:
        count=0
        dates=set()
        post_date=[]
        months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
        pId=1
        for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
            threadId=smart_str(entry["threadId"])
            topics=list(entry["topics"])
            if str(T) in topics:
                for post in posts.find({"threadId" : threadId}, timeout=False):
                    postdate=smart_str(post["date"])
                    month= [months[key] for key in months.keys() if postdate[:3] in key]
                    try:
                        day=int(postdate[5:7])
                    except ValueError:
                        day=int(postdate[5:6])
                    year=int(postdate[8:])
                    d=date(year,month.pop(),day)
                    dates.add(d)
                    threadId=smart_str(post["threadId"])
                    postId=smart_str(post["postId"])
                    text=smart_str(post["text"])
                    if(postId==""):
                        postId=pId
                        pId+=1
                    post_date.append((threadId,postId,d, text))
                    count+=1
                #print "post", count, len(post_date)
                
        dates=list(dates)
        oldest_date=min(dates)
        youngest_date=max(dates)
        print "Oldest date", oldest_date
        print "Youngest date", youngest_date
    
        start=oldest_date
        timeslots=[]
        while start<=youngest_date:
            end=start+relativedelta(months = +6)
            timeslots.append((start,end))
            start=end
        num_timeslots=len(timeslots)
        print num_timeslots, timeslots 
        slots=[]
        i=0
        while i<num_timeslots:
            slots.append([])
            i+=1
        print "Num of slots", len(slots), num_timeslots
        
        postcount=0
        for entry in post_date:
            i=0
            while i<num_timeslots:
                if entry[2]>=timeslots[i][0] and entry[2]< timeslots[i][1]:
                    postcount+=1
                    slots[i].append(entry[3])
                i+=1
       
        tslot=[]
        all_tokens=[]
        for slot in slots:
            string=""
            for text in slot:
                string+=text+" "
            tokens=re.findall("\\w{3,}",string.strip())
            new_tokens=[]
            for token in tokens:
                token=token.lower()
                if token not in stopwords:
                    new_tokens.append(token)
                    all_tokens.append(token)
            wordcount=Counter()
            for word in new_tokens :
                wordcount[word]+=1
            print "Total number of unique unigrams in this slot", len(wordcount)
            tslot.append(wordcount)
        print "Slots", len(tslot)
        
        totalwordcount=Counter()
        for word in all_tokens:
            totalwordcount[word]+=1
        totalwordcount=dict(totalwordcount)
        for k, value in sorted(totalwordcount.items(), key=lambda x: x[1], reverse=True): #sorting by value
                maxtermfreqcorpus=value
                break
    
        print "Total number of unique unigrams in the entire corpus", len(totalwordcount)
        i=0
        totalwords=0
        g=open("/media/netdisk/ansuya/top10subscoreperslottopic{0}_1.txt".format(T),"w")
        g.write("word   (term_freq_slot/max_term_freq_slot)-(term_freq_corpus/mex_term_freq_corpus)\n")
        for slot in tslot:
            words=slot.keys()
            word_subscore=[]
            slot=dict(slot)
            for k, value in sorted(slot.items(), key=lambda x: x[1], reverse=True):
                maxtermfreqslot=value
                break
            for word in words:
                slottermcount=slot[word]
                totaltermcount=totalwordcount[word]
                sub_score= (float(slottermcount)/float(maxtermfreqslot))-(float(totaltermcount)/float(maxtermfreqcorpus))
                word_subscore.append((word,sub_score))
                totalwords+=1
            
            d=dict(word_subscore)
            sorted_d=sorted(d.items(), key=lambda x: x[1], reverse=True)
            sorted_d=sorted_d[:20]
            g.write("slot ")
            g.write(str(i))
            g.write("\n")
            for entry in sorted_d:
                g.write(entry[0])
                #g.write("\t")
                #g.write(str(entry[1]))
                g.write("\n")
            i+=1
        g.close()
        print "Total unigrams added to different slots", totalwords
        T+=1
    
def topusers():
    global tt
    f=open("/media/netdisk/ansuya/cafemomwork/CafemomTimeSlots.txt","r")
    slot_user_topics=[]
    slot_user=[]
    c=0 
    for line in f:
        slot=line.split("\t")[0]
        if c==0:
            prevSlot=slot
            slotu=[]
            slotut=defaultdict(list)
        threadId=line.split("\t")[1]
        userId=line.split("\t")[2]
        for entry in tt.find({"threadId":threadId},timeout=False):
            if float(smart_str(entry["maxProportion"])) > 0.3 :
                topics=list(entry["topics"])
            else:
                topics=[]
        if slot!=prevSlot:
            slot_user.append(slotu)
            slot_user_topics.append(dict(slotut))
            slotu=[]
            slotut=defaultdict(list)
        elif slot==prevSlot:
            slotu.append(userId)
            slotut[userId].extend(topics)
        c+=1
        prevSlot=slot
        print c
    slot_user.append(slotu)
    slot_user_topics.append(dict(slotut))        
    
    print len(slot_user), len(slot_user_topics)
    
    slot_user_unique=[]
    for slot in slot_user:
        usercount=Counter()
        for user in slot :
            usercount[user]+=1
        print "Total number of unique users in this slot", len(usercount)
        slot_user_unique.append(dict(usercount))
    print "Slots", len(slot_user_unique)
    
    g=open("/media/netdisk/ansuya/cafemomwork/topicusersperslot.txt","w")
    i=0
    u=0
    for slot1, slot2 in zip(slot_user_unique, slot_user_topics):
        sorted_d=sorted(slot1.items(), key=lambda x: x[1], reverse=True)
        sorted_d=sorted_d[:500]
        g.write("slot ")
        g.write(str(i))
        g.write("\n")
        for entry in sorted_d:
            g.write(entry[0])
            g.write("\t")
            g.write(str(entry[1]))
            g.write("\t")
            if (slot2[entry[0]]):
                topics=list(set(slot2[entry[0]]))
                #print topics
                j=0
                for topic in topics:
                    g.write(str(topic))
                    if j<len(topics)-1:
                        g.write(",")
                    j+=1
            g.write("\n")
            u+=1
        i+=1
    g.close()
    print "Total users added to different slots", u

def slotusers():
    f=open("/media/netdisk/ansuya/cafemomwork/CafemomTimeSlots.txt","r")
    g=open("/media/netdisk/ansuya/cafemomwork/R/userfreq.txt","w")
    slotdu=Counter()
    c=0 
    for line in f:
        date=line.split("\t")[4][:7]
        date+="-01"
        if c==0:
            prevDate=date
            slotu=set()
        userId=line.split("\t")[2]
        if date!=prevDate:
            slotu=list(slotu)
            u=len(slotu)
            while u!=0:
                slotdu[date]+=1
                g.write(str(date))
                g.write("\n")
                u-=1
            slotu=set()
        slotu.add(userId)
        prevDate=date
        c+=1
        print c
    slotu=list(slotu)
    u=len(slotu)
    while u!=0:
        slotdu[date]+=1
        g.write(str(date))
        g.write("\n")
        u-=1      
    
    print dict(slotdu), len(slotdu)
    g.close()
    f.close()
         
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
tt=Cafemomdb.threadtopic1
log = open("mongoError.log","a")
#stopwords=[]
#sw=open("/media/netdisk/ansuya/mallet-2.0.7/stoplists/en.txt","r")
#for line in sw:
#    stopwords.append(line[:-1])
#sw.close()
#topicthreads()
#tfidf()
#subcount()
topusers()
#slotusers()
log.close()
