#!/usr/local/bin/python

# This program reads data collected from mothering.com and enters it in MongoDB database called Mothering. 
# March 2012

from pymongo import Connection
import re
connection = Connection()
motheringdb = connection.Mothering
posts = motheringdb.posts

f = open("/media/netdisk/zzhou/vaccination/MegTable2.txt")
log = open("mongoError.log","a")

g=open("/home/ansuya/MotheringData/LinksMothering.txt","r")
PosLink=[]
c=0
for line in g:
    if(line[0]=='P'):
        postid=line[9:]
    elif(line[0]=='L'):
        links=re.findall("http://.+? |https://.+? ",line[7:])
        PosLink.append((postid,links))
        c=c+1
#print c
g.close()

g=open("/home/ansuya/MotheringData/PostDomsMothering.txt","r")
PosDom=[]
d=0
for line in g:
    if(line[0]=='P'):
        postid=line[9:]
        #print postid
    elif(line[0]=='D'):
        domains=re.findall(".+? ",line[9:])
        PosDom.append((postid,domains))
        d=d+1
#print d
g.close()

g=open("/media/netdisk/zzhou/vaccination/SentTable.txt").read()
posscore=re.findall("(.+?)\\s+?.+?\\s+?.+?\\s+?.+?\\s+?(.+?)\\s",g)
#print len(posscore)
h=open("/media/netdisk/zzhou/vaccination/PostLength.txt").read()
poslen=re.findall("(.+?)\\t(.+?)\\s",h)
#print len(poslen)

i = 0
for line in f:
    
     tag = (line.split(':')[0])
     wholevalue = line.split('\n')[0]
     value=re.search("(?<=:).*",wholevalue).group().strip()
     if tag =="PostId": post_id = value
     elif tag == "Time": 
        time = re.search("(?<=at ).+",value).group()
        date = re.search(".+?(?= at)",value).group()
     elif tag == "ThreadId": thread_id = value
     elif tag =="Title": title = value
     elif tag=="UserId": user_id=value
     elif tag=="MetaData": 
        order=re.search("(?<=post #).+?(?=of)",value).group()
     elif tag=="Text": text=value              
     elif tag =="Quote": 
        i+=1
        quote = value
        for plink, pdom in zip(PosLink,PosDom):
            if(plink[0]==post_id+"\n" and pdom[0]==post_id+"\n"):
                for pscore in posscore:
                    if(pscore[0]==post_id):
                        break
                for plen in poslen:
                    if(plen[0]==post_id):
                        break
                new_record = [{ "postId" : post_id, "date" : date, "time" :time, "threadId" : thread_id, "title" : title, "userId" : user_id, "orderInThread": order, "text": text, "quote": quote, "links": plink[1], "domains": pdom[1], "sentScore": pscore[1], "postLength": plen[1]}]
                posts.insert(new_record)
                print i
     #     print new_record
#     except:
#          log.write(line)
#          continue
     

print "Total entries processed = " + str(i)
f.close()
log.close()

