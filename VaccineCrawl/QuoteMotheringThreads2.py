#!urs/local/bin/python
#-*- coding: utf-8 -*
import re
import urllib
import pickle
import sys
import os

sys.setrecursionlimit(100000)

def readUrls():
    textfile=0
    while(textfile!=5):
#        f=open("/media/netdisk/zzhou/mothering/test.dat","r")
  	f=open("/media/netdisk/zzhou/mothering/html/HtmlChunk{0}.dat".format(textfile),"r")
        count=0
        page='' 
	counter=0
        for line in f:
	    line=line.strip();
            if(line!= "***** mothering site crawler *******html content download********copyright Zicong Zhou****" or line!="</html>"):
            	page=page+line
            if(line=="</html>"):
                thread_no=re.search("(?s)(?<=community/t/)(.*?)(?=/.+?<!DOCTYPE html>)|(?<=community/forum/thread/)(.*?)(?=/.+?<!DOCTYPE html>)",page).group()
                print "THREAD",thread_no
                count=count+1
                print "THREAD COUNT", count
                parsePage(page,thread_no)
                page=''
        f.close()
        textfile=textfile+1
    print "THREAD COUNT", count
      
def parsePage(thread,thread_no):
#    f=open("motheringsite2/MotheringThread{0}.txt".format(thread_no),"a+")
    f=open("/media/netdisk/motheringsite/MotheringThread{0}.txt".format(thread_no),"a")
    if(os.stat("/media/netdisk/motheringsite/+MotheringThread{0}.txt".format(thread_no))[6]==0):
        title=re.search("(?s)<h1 class=\"forum-h1\">.*?</h1>",thread)
        f.write("THREAD_TITLE: ")
        f.close()
        text1(title.group(),0,thread_no)
    else:
        f.close()
    text(thread,thread_no)
    
def text(page,thread_no):
    posts=re.findall("(?s)(<div id=\"post_(\\d+?)\".+?(?=<div id=\"post_|<div id=\"control-btm\"))",page)
    for post in posts:
        text1(post[0],post[1],thread_no)
          
def text1(post,post_id,thread_no):
    f=open("/media/netdisk/motheringsite/MotheringThread{0}.txt".format(thread_no),"a")
    usr_id=re.findall("<a rel=\"nofollow\" href=\"/community/u/(.+?)/.+?\" class=\"thumb\">",post)
    ##print usr_id
    remain=0
    remain2=0
    q_text1=[]
    q_text2=[]
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            ##print"1111: ", m.group(),"\n"
            q1=re.search("(?s)<div class=\"smallfont\" style=\"margin-bottom:2px;\">",m.group())
            q2=re.search("(?s)<div class=\"quote-container\">",m.group())
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            if(q1!=None or remain==1):
                remain=1
                q_text1.append(l.group().strip().replace('\n',' '))
                q_text1.append(' ')
                if(re.search("</table>",m.group())!=None):
                    remain=0
            if(q2!=None or remain2==1):
                remain2=1
                q_text2.append(l.group().strip().replace('\n',' '))
                q_text2.append(' ')
                if(re.search("</div>",m.group())!=None):
                    remain2=0
            if(n==None and remain==0 and remain2==0):
                ##print"2222: ", l.group()
		        if(re.search("<div id=\"post_",m.group())!=None):
		            f.write("\nMETA DATA: ")
		            f.write("user_id=")
		            f.write(usr_id.pop())
		            f.write(' ')
		            f.write("post_id=")
		            f.write(post_id)
		            f.write(' ')
		            f.write(l.group().strip().replace("\n"," "))
		            f.write(' ')
		        elif(re.search("(?s).*?Select All Posts By This User*?",l.group())!=None):
		            f.write(l.group().strip().replace("\n"," "))
		            f.write(' ')
		            f.write("\nTEXT: ")
		        else:
		            f.write(l.group().strip().replace("\n"," "))
		            f.write(' ')              
    if(post_id!=0):
        f.write("\nQUOTE: ")
        if(q_text1):
            for word in q_text1:
                f.write(word)
        elif(q_text2):
            for word in q_text2:
                f.write(word)
                         
    f.close()
    
readUrls()

