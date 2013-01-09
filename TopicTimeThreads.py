from pymongo import Connection
from pymongo import errors
from django.utils.encoding import smart_str, smart_unicode
from datetime import date
from dateutil.relativedelta import relativedelta

connection = Connection()
Cafemomdb = connection.Cafemom
posts = Cafemomdb.posts
tt=Cafemomdb.threadtopic1
log = open("mongoError.log","a")

#topic0=[]
#topic1=[]
#topic2=[]
#topic3=[]
#topic4=[]
#topic5=[]
#topic6=[]
#topic7=[]
topic8=[]
#topic9=[]
months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
timeslots= [(date(2007,2,6),date(2007,8,6)),
(date(2007,8,6),date(2008,2,6)),
(date(2008,2,6),date(2008,8,6)),
(date(2008,8,6),date(2009,2,6)),
(date(2009,2,6),date(2009,8,6)),
(date(2009,8,6),date(2010,2,6)),
(date(2010,2,6),date(2010,8,6)),
(date(2010,8,6),date(2011,2,6)),
(date(2011,2,6),date(2011,8,6)),
(date(2011,8,6),date(2012,2,6)),
(date(2012,2,6),date(2012,8,6))]
#print timeslots
for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
    threadId=smart_str(entry["threadId"])
    topics=list(entry["topics"])
    if "8" in topics:
        for post in posts.find({"threadId" : threadId}, timeout=False):
            #print post
            postdate=smart_str(post["date"])
            month= [months[key] for key in months.keys() if postdate[:3] in key]
            try:
                day=int(postdate[5:7])
            except ValueError:
                day=int(postdate[5:6])
            year=int(postdate[8:])
            d=date(year,month.pop(),day)
            i=0
            while i<11:
                if d>=timeslots[i][0] and d<= timeslots[i][1]:
                    f=open("/media/netdisk/ansuya/topic8timeslots/slot{0}/data/{1}.txt".format(i,threadId),"a")
                    f.write(smart_str(post["text"]))
                    f.write("\n")
                    f.close()  
                i+=1            
log.close()
