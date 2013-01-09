import sys
from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
sys.setrecursionlimit(1000000)

connection = Connection()
Cafemomdb = connection.Cafemom
users = Cafemomdb.users
log = open("mongoError.log","a")

f=open("/media/netdisk/cafemomfriends.txt","r")
g=open("/media/netdisk/cafemomfriendsinclude.txt","w")
h=open("/media/netdisk/cafemomfriendsexclude.txt","w")

userNames=[]
userIds=[]
for user in users.find():
    userId=smart_str(user["userId"])
    userName=smart_str(user["userName"])
    userNames.append(userName)
    userIds.append(userId)
notinusers=0    
includedusers=0
for line in f:
    users=line.split("\t")
    mainuser=users[0]
    users.remove(mainuser)
    s=0
    t=0
    for friend in users:
        if friend[1:-1] in userNames :
            if s==0: 
                g.write(mainuser)
                g.write("\t")
                s=1
                includedusers+=1
                print includedusers
            i=userNames.index(friend[1:-1])
            g.write(userIds[i])
            g.write("\t")
        else:
            if t==0:
                h.write(mainuser)
                h.write("\t")
                t=1
            h.write(friend)
            h.write("\t")
            notinusers+=1
    if s==1 : g.write("\n")
    if t==1: h.write("\n")
print "Repeated Friends who weren't in users table", notinusers    
print "Total users in users table", len(userNames), len(userIds)
print "Users with friends present in users table", includedusers
f.close()
g.close()
h.close()
