#Code to extract data from Cafemom database and save it in format required for topic modeling
# Saved text for each post in a separate text file with filename as post Id
from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
threads=Cafemomdb.threads
log = open("mongoError.log","a")
enteries=0
thread=set()
threadgroup=[]
for thread in threads.find():
    threadId=smart_str(thread["threadId"])
    groupId=smart_str(thread["groupId"])
    threadgroup.append((threadId,groupId))
    
for post in posts.find():
    data=smart_str(post["text"])+"\n"
    postId=smart_str(post["postId"])
    threadId=smart_str(thread["threadId"])
    if(len(data.split(" "))>10):
        for entry in threadgroup:
            if threadId==entry[0]:
                groupId=entry[1]
        f=open("/media/netdisk/cafemomless1/data/{0}-{1}-{2}.txt".format(groupId,threadId,postId),"a")
        f.write(data)
        f.write("\n")
        #if threadId not in thread:
            #thread.add(threadId)
        enteries+=1
        print enteries
        f.close()

print "Total enteries in threads table", len(threadgroup)
print "Total enteries saved", enteries
#print "Total threads", len(thread)

#count average thread length
#enteries=0
#total=0
#for entry in ppt.find():
#    total+=float((smart_str(entry["value"]["recs"])))
#    enteries+=1
#print "avg", data/enteries
#avg 12.1909289735

log.close()
