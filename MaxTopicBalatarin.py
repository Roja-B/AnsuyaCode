from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
connection = Connection()
Cafemomdb = connection.Cafemom
tt = Cafemomdb.threadtopic1
#tsst=Cafemomdb.threadstopstemtopic

log = open("mongoError.log","a")

def insert_record(record,table):
    new_record = [{ "threadId" : record[0], "topics": record[1], "maxProportion" : record[2] }]
    table.insert(new_record) 
        
def maxtopicprop(f,table):
    #g=open('/media/netdisk/mallet-2.0.7/cafemomthreadmaxtopicprop.txt','w')
    count=0
    topicprops=[]
    
    for line in f:
        count+=1
        print count
        topics=[]
        record=[]
        #print line.split('\t'), len(line.split('\t'))# compare value at index 3 to all values at odd indices upto 21
        if count > 1 :
            l=line.split('\t')
            #print l
            ##if table==tlt:
            ##    threadId=l[1].split('/')[6].split('.')[0]
            ##elif table==tst:
            threadId=l[1].split('/')[6].split('.')[0]
            #print threadId
            #g.write(threadId)
            #g.write('\t')
            #g.write(l[2])
            topics.append(l[2])
            i=5
            topicprops.append(float(l[3]))
            while i<13:
                if l[3]==l[i]:
                    topics.append(l[i-1])
                    #g.write(',')
                    #g.write(l[i-1])    
                i+=2
            #g.write('\t')
            #g.write(l[3])
            #g.write('\n')
            record.append(threadId)
            record.append(topics)
            record.append(l[3])
            #print record
            insert_record(record,table)
                    
    print max(topicprops)
    print min(topicprops) 
    print sum(topicprops)/float(len(topicprops))
    #g.close()            

f=open('/media/netdisk/ansuya/mallet-2.0.7/cafemomthread1doctopics','r')#cafemomthreaddoctopics','r')
maxtopicprop(f,tt)
f.close()
#f=open('/media/netdisk/mallet-2.0.7/cafemomthreadstopstemdoctopics','r')
#maxtopicprop(f,tsst)
#f.close()
