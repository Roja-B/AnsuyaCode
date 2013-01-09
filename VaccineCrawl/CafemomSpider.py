#!urs/local/bin/python
#-*- coding: utf-8 -*-
import re, urllib

base_url="http://www.cafemom.com"
group_no=1
f=open("/home/ansuya/CafemomData/CafemomGroupLinks.txt","a")
def extractpage(URL,f):
    global group_no
    page=urllib.urlopen(URL).read()
    group_links=re.findall("(?s)<div class=\"groupDescription\">[\\n\\s*?]<h4><a href=\"(.+?)\">",page)
    for link in group_links:
        f.write(base_url+link)
        f.write("\n")
        print group_no
        group_no+=1
    #next_page=re.search("((?<=<a href=\")([^&;]+?&amp;[^amp]+?)(?=\" class=\"standardBtn btnGreen nextprev next\">next</a>))",page)
   
    #if(next_page):
        #print next_page.group()
        #URL=base_url+next_page.group()
        #print URL
        #extractpage(URL,f)
    #f.close()
    
extractpage("http://www.cafemom.com/groups/find.php?keyword=vaccine",f)
URL="http://www.cafemom.com/groups/find.php?keyword=vaccine&amp;&next=11"
extractpage(URL,f)
f.close()
