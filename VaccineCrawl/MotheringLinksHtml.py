import urllib2, httplib

def readUrls():
    textfile=0
    count=0
    while(textfile!=5):
#        f=open("/media/netdisk/zzhou/mothering/test.dat","r")
  	f=open("/media/netdisk/zzhou/mothering/html/HtmlChunk{0}.dat".format(textfile),"r")
        
        page=''
        for line in f:
	    line=line.strip();
            if(line!= "***** mothering site crawler *******html content download********copyright Zicong Zhou****" or line!="</html>"):
            	page=page+line
            if(line=="</html>"):
                count=count+1
                print "THREAD COUNT", count
                text(page)
                page=''
        f.close()
        textfile=textfile+1
    #print "THREAD COUNT", count
    
def text(page):
    global l
    posts=re.findall("(?s)(<div id=\"post_\\d+?\".+?(?=<div id=\"post_|<div id=\"control-btm\"))",page)
    for post in posts:
        links=re.findall("<a href=\"([^\\s]+?)\" target=\"_blank\">",post)
        if(links):
            #print links
            l.extend(links)
        
count=0
errorcount=0
wcount=0
l=[]
readUrls()
l=list(set(l))
f=open("/media/netdisk/MotheringLinksHtml.txt","a")
for entry in l:
    try:
        req=urllib2.urlopen(entry,None,10)
        page=req.read()
        wcount+=1
        returnUrl=req.geturl()
        if(entry!=returnUrl):
            print entry ,"redirected to", returnUrl
            f.write("\n****mothering-mentioned link****html content download****\n")
            f.write(entry)
            f.write("\n")
            f.write(page)
    except (IOError, ValueError, AttributeError, httplib.BadStatusLine, httplib.IncompleteRead,httplib.InvalidURL):
        print "Erroneous host   ",entry
        errorcount+=1
    count+=1
    print count
print "Error count", errorcount
print "Links visited", wcount
print "Total links", len(l)
f.close()
