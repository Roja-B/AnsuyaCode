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

topic0=[]
topic1=[]
topic2=[]
topic3=[]
topic4=[]
topic5=[]
topic6=[]
topic7=[]
topic8=[]
topic9=[]

#months={"Jan": 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6, "Jul" : 7, "Aug" : 8, "Sep" :9, "Oct" : 10, "Nov" : 11, "Dec" : 12}

for entry in tt.find({"maxProportion":{"$gt" : "0.3"}},timeout=False):
    threadId=smart_str(entry["threadId"])
    for post in posts.find({"threadId" : threadId}, timeout=False):
        #print post
        topics=list(entry["topics"])
        #postdate=smart_str(post["date"])
        #month= [months[key] for key in months.keys() if postdate[:3] in key]
        #try:
        #    day=int(postdate[5:7])
        #except ValueError:
        #    day=int(postdate[5:6])
        #year=int(postdate[8:])
        #d=date(year,month.pop(),day)
	d=smart_str(post["userId"])
        for topic in topics:
            if topic =='0' :
                topic0.append(d)
                print "added to topic 0"
            elif topic == '1':
                topic1.append(d)
                print "added to topic 1"
            elif topic == '2':
                topic2.append(d)
                print "added to topic 2"
            elif topic == '3':
                topic3.append(d)
                print "added to topic 3"
            elif topic == '4':
                topic4.append(d)
                print "added to topic 4"
            elif topic == '5':
                topic5.append(d)
                print "added to topic 5"
            elif topic == '6':
                topic6.append(d)
                print "added to topic 6"
            elif topic == '7':
                topic7.append(d)
                print "added to topic 7"
            elif topic == '8':
                topic8.append(d)
                print "added to topic 8"
            elif topic == '9':
                topic9.append(d)
                print "added to topic 9"

print len(list(set(topic0))), len(list(set(topic1))), len(list(set(topic2))), len(list(set(topic3))), len(list(set(topic4))) , len(list(set(topic5))),len(list(set(topic6))), len(list(set(topic7))), len(list(set(topic8))), len(list(set(topic9)))  
i=0
#while i<10:
    #f=open("/media/netdisk/ansuya/cafemomwork/R/topic{0}.txt".format(i),"w")
    #f.write("date")
    #f.write("\n")
    #if i==0:
    #    for d in topic0:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==1:
    #    for d in topic1:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==2:
    #    for d in topic2:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==3:
    #    for d in topic3:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==4:
    #    for d in topic4:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==5:
    #    for d in topic5:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==6:
    #    for d in topic6:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==7:
    #    for d in topic7:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==8:
    #    for d in topic8:
    #        f.write(str(d))
    #        f.write("\n")
    #elif i==9:
    #    for d in topic9:
    #        f.write(str(d))
    #        f.write("\n")
    #f.close()
    #i+=1
log.close()               
