#!urs/local/bin/python
#-*- coding: utf-8 -*
import re
import urllib
import pickle
import sys

sys.setrecursionlimit(100000)

def readUrls():
    textfile=0
    count=0
    while(textfile!=5):
        f=open("/media/netdisk/zzhou/mothering/html/HtmlChunk{0}.dat".format(textfile),"r")
        page=''
        for line in f:
            line=line.strip()
            if(line!= "***** mothering site crawler *******html content download********copyright Zicong Zhou****" or line!="</html>"):
                page=page+line
            if(line=="</html>"):
                count=count+1
                ##print "THREAD COUNT", count
                parsePage(page)
                page=''
        f.close()
        textfile=textfile+1
    print "THREAD COUNT", count
      
def parsePage(thread):
    title=re.search("(?s)<h1 class=\"forum-h1\">.*?</h1>",thread)
    text(thread)
    
def text(page):
    posts=re.findall("(?s)(<div id=\"post_(\\d+?)\".+?(?=<div id=\"post_|<div id=\"control-btm\"))",page)
    for post in posts:
        text1(post[0],post[1])
          
def text1(post,post_id):
    f=open("EmoticonMothering.txt","a+")
    usr_id=re.findall("<a rel=\"nofollow\" href=\"/community/u/(.+?)/.+?\" class=\"thumb\">",post)
    ##print usr_id
    remain=0
    remain2=0
    emoticon=[]
    for m in re.finditer("(?#all text)(?s)<(?=[^(!--)]).+?>.*?(?=<)",post):
        if(m!=None):
            ##print"1111: ", m.group(),"\n"
            q1=re.search("(?s)<div class=\"smallfont\" style=\"margin-bottom:2px;\">",m.group())
            q2=re.search("(?s)<div class=\"quote-container\">",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            if(q1!=None or remain==1):
                remain=1
                if(re.search("</table>",m.group())!=None):
                    remain=0
            if(q2!=None or remain2==1):
                remain2=1
                if(re.search("</div>",m.group())!=None):
                    remain2=0
            if(n==None and remain==0 and remain2==0):
		        emo=re.search("(?s)<img alt=\".+?.gif\" id=\"user_.+?\" src=\".+?.gif\">",m.group())
		        if(emo!=None):
		            emoticon.append(emo.group())
	emoticon.reverse()
	if(emoticon):
	    f.write("\nPOST_ID: ")
	    f.write(post_id)
	    f.write("\nEMOTICONS: ")
	    while(emoticon):
	        f.write(emoticon.pop())
	        f.write(" ")	            
                         
    f.close()
    
readUrls()

