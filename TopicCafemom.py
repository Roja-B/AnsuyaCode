#Code to extract data from Cafemom database and save it in format required for topic modeling
# Saved text for each post in a separate text file with filename as post Id
from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
log = open("mongoError.log","a")
enteries=0
thread=set()
for post in posts.find():
    data=smart_str(post["text"])+"\n"
    threadId=smart_str(post["threadId"])
    if(len(data.split(" "))>0):
        f=open("/media/netdisk/cafemomthread/data/{0}.txt".format(threadId),"a")
        f.write(data.strip()+" ")
        if threadId not in thread:
            thread.add(threadId)
        enteries+=1
        print enteries
        f.close()

print "Total enteries saved", enteries
print "Total threads", len(thread)

#count average thread length
#enteries=0
#total=0
#for entry in ppt.find():
#    total+=float((smart_str(entry["value"]["recs"])))
#    enteries+=1
#print "avg", data/enteries
#avg 12.1909289735

log.close()
