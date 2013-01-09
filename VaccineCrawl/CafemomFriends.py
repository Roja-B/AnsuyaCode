import twill.commands
from mechanize import BrowserStateError
import re
import sys
from pymongo import Connection
from django.utils.encoding import smart_str, smart_unicode
sys.setrecursionlimit(1000000)

def findfriends(url,userfriends,g):
    global start
    global i
    global nop
    global start_url
    try:
        b.go(url)
        page=b.get_html()
        friends=re.findall("<a href=\"/home/(.+?)\">",page)
        friends.remove("complexnetworks")
        if start==0:
            totalfriends=re.findall("<div class=\"paginationCount spaceBottom5\">.+?\\sof\\s(\\d+)",page)
            if totalfriends:
                tf=totalfriends.pop()
                print "Number of friends",tf
                num=int(tf)
                nop=(num/25)
        start=1
        if friends:
            userfriends.extend(friends)
            #next_page=re.search("((?<=<a href=\")([^\\s]+?)(?=\" class=\"standardBtn btnGreen nextprev next\">next</a>))",page)
            if nop!=0:
                i+=25
                next_page_link=start_url+"&next="+str(i)
                nop-=1
                if next_page_link!=url:
                    findfriends(next_page_link,userfriends,g)
    except BrowserStateError:
        pass
        #g.write(url)
        #g.write("\n")
    return userfriends
    
connection = Connection()
Cafemomdb = connection.Cafemom
users = Cafemomdb.users
log = open("mongoError.log","a")
base_url="http://www.cafemom.com"
b = twill.commands.get_browser()
url = "http://www.cafemom.com/login.php"
b=twill.commands.get_browser()
b.go(url)
form=b.get_form("2")
form["identifier"]="complexnetworks"
form["password"]="ansuya"
b.clicked(form,"None")
b.submit()
friend_url="http://www.cafemom.com/network/friends.php?user_id="
f=open("/media/netdisk/cafemomfriends.txt","a")
#g=open("/media/netdisk/failedcafemomfriends.txt","a")
enteries=19120
start=0
nop=0
i=1
s=0
for user in users.find():
    userId=smart_str(user["userId"])
    if(userId=="196444" or s==1):
        s=1
        userfriends=[]
        url=friend_url+userId
        start_url=url
        userfriends=findfriends(url,userfriends,g)
        start=0
        i=1
        if userfriends:
            print "User number", enteries
            f.write(userId)
            f.write("\t")
            for userfriend in userfriends:
                f.write("\"")
                f.write(userfriend)
                f.write("\"")
                f.write("\t")
            f.write("\n")
            enteries+=1
    
     
b.go("http://www.cafemom.com/logout.php")
f.close()
#g.close()
log.close()
