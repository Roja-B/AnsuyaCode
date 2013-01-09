#Code to find the oldest and youngest date from all posts in Cafemom database
from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta

def addtofile(cluster,f):
    global enteries,i
    #threads=[]
    cluster=list(set(cluster))
    for entry in cluster: #time_cluster threadId userId postId date
        f.write(str(i))
        f.write("\t")
        f.write(entry)#(entry[0])
        #threads.append(entry[0])
        #f.write("\t")
        #f.write(entry[3])
        #f.write("\t")
        #f.write(str(entry[2]))
        #f.write("\t")
        #f.write(str(entry[1]))
        ##f.write("\n")
        ##enteries+=1
    i+=1
    #print "Number of posts from cluster", i, " is ", len(cluster)
    print "Number of unique threads from cluster", i, "is", len(cluster)#len(list(set(threads)))
        
connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
log = open("mongoError.log","a")
enteries=0
dates=set()
post_date=[]
months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
pId=1
for post in posts.find():
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
    if(postId==""):
        postId=pId
        pId+=1
    userId=smart_str(post["userId"])
    post_date.append((threadId,d,postId,userId))
    enteries+=1
print enteries, pId-1

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
print timeslots 

cluster1=[]
cluster2=[]
cluster3=[]
cluster4=[]
cluster5=[]
cluster6=[]
cluster7=[]
cluster8=[]
cluster9=[]
cluster10=[]
cluster11=[]  

#for entry in post_date:
#    if entry[1] >= timeslots[0][0] and entry[1] < timeslots[0][1]: cluster1.append(entry[0])#cluster1.append(entry)
#    elif entry[1] >= timeslots[1][0] and entry[1] < timeslots[1][1]: cluster2.append(entry[0])#cluster2.append(entry)
#    elif entry[1] >= timeslots[2][0] and entry[1] < timeslots[2][1]: cluster3.append(entry[0])#cluster3.append(entry)
#    elif entry[1] >= timeslots[3][0] and entry[1] < timeslots[3][1]: cluster4.append(entry[0])#cluster4.append(entry)
#    elif entry[1] >= timeslots[4][0] and entry[1] < timeslots[4][1]: cluster5.append(entry[0])#cluster5.append(entry)
#    elif entry[1] >= timeslots[5][0] and entry[1] < timeslots[5][1]: cluster6.append(entry[0])#cluster6.append(entry)
#    elif entry[1] >= timeslots[6][0] and entry[1] < timeslots[6][1]: cluster7.append(entry[0])#cluster7.append(entry)
#    elif entry[1] >= timeslots[7][0] and entry[1] < timeslots[7][1]: cluster8.append(entry[0])#cluster8.append(entry)
#    elif entry[1] >= timeslots[8][0] and entry[1] < timeslots[8][1]: cluster9.append(entry[0])#cluster9.append(entry)
#    elif entry[1] >= timeslots[9][0] and entry[1] < timeslots[9][1]: cluster10.append(entry[0])#cluster10.append(entry)
#    elif entry[1] >= timeslots[10][0] and entry[1] < timeslots[10][1]: cluster11.append(entry[0])#cluster11.append(entry)

#f=open("/media/netdisk/ansuya/cafemomwork/CafemomTimeSlots1.txt","r")
#enteries=0
#i=0
#addtofile(cluster1,f)
#addtofile(cluster2,f)
#addtofile(cluster3,f)
#addtofile(cluster4,f)
#addtofile(cluster5,f)
#addtofile(cluster6,f)
#addtofile(cluster7,f)
#addtofile(cluster8,f)
#addtofile(cluster9,f)
#addtofile(cluster10,f)
#addtofile(cluster11,f)
#f.close()
#print "Total posts added", enteries
log.close()
