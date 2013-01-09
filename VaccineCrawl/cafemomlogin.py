import twill.commands
import re
import sys
sys.setrecursionlimit(1000000)

def extractforums():
    global b
    f=open("/home/ansuya/CafemomData/CafemomGroupLinks.txt","r")
    g=open("/home/ansuya/CafemomData/CafemomForumLinks.txt","a")
    for line in f:
        b.go(line)
        page=b.get_html()
        forum_links_block=re.search("(?s)<ul class=\"clearfix dotDividerSmall whiteDot\">.+?(?=<a href=\"/group/\\d+/photos/\">)",page).group()
        forum_links=re.findall("(?s)<a href=\"([^\\s]+?)\">",forum_links_block)
        for forum_link in forum_links:
            forum_link=base_url+forum_link
            g.write(forum_link)
            g.write("\n")
    g.close()
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
#form=b.get_form("1")
#form["keyword"]="vaccination"
#b.clicked(form,"None")
#b.submit()
extractforums()   
b.go("http://www.cafemom.com/logout.php")
