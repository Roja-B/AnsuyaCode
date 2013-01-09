import twill.commands
import re
import sys
sys.setrecursionlimit(1000000)

def readforumlinks():
    global b
    f=open("/home/ansuya/CafemomData/CafemomForumLinks.txt","r")
    for line in f:
        b.go(line)
        page=b.get_html()
        extractthreadlinks(page)
    f.close()
    
def extractthreadlinks(page):
    global threadlinks, count, b
    thread_link_blocks=re.findall("(?s)<td class=\"post\">.+?</div>",page)
    if(thread_link_blocks):
        for thread_link_block in thread_link_blocks:
            thread_link=re.search("(?<=<a href=\")([^\\s]+?)(?=\">)",thread_link_block).group()
            thread_link=base_url+thread_link
            count=count+1
            threadlinks.append(thread_link)
    next_page=re.search("((?<=<a href=\")([^\\s]+?)(?=\" class=\"standardBtn btnGreen nextprev next\">next</a>))",page)
    if(next_page):
        next_page_link=base_url+next_page.group()
        b.go(next_page_link)
        page=b.get_html()
        extractthreadlinks(page)
    else:
        return None
        
def savethreadhtml():
    global b, threadpages
    #, threadlinks
    count=0
    f=open("/home/ansuya/CafemomData/CafemomThreadLinks.txt","r")
    h=open("/media/netdisk/cafemomsite/CafemomThreadHtml.txt","a")
    for line in f:
        b.go(line)
        page=b.get_html()
        h.write("\n****cafemom site****html content download****\n")
        h.write(line)
        h.write("\n")
        h.write(page)
        threadpages+=1
        next_reply_page=re.search("((?<=<a href=\")([^\\s]+?)(?=\" class=\"standardBtn btnGreen nextprev next\">next</a>))",page)
        while(next_reply_page):
           next_reply_page_link=base_url+next_reply_page.group()
           b.go(next_reply_page_link)
           page=b.get_html()
           h.write("\n****cafemom site****html content download****\n")
           h.write(next_reply_page_link)
           h.write("\n")
           h.write(page)
           threadpages+=1
           next_reply_page=re.search("((?<=<a href=\")([^\\s]+?)(?=\" class=\"standardBtn btnGreen nextprev next\">next</a>))",page)
    h.close()
    f.close()
    
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
#count=0
threadpages=0
#threadlinks=[]
#readforumlinks() 
#g=open("/home/ansuya/CafemomData/CafemomThreadLinks.txt","a")
#for link in threadlinks:
#    g.write(link)
#    g.write("\n")  
#g.close()
#print "Thread count", count
savethreadhtml()
print "Thread pages", threadpages
b.go("http://www.cafemom.com/logout.php")
