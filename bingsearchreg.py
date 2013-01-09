#!/urs/local/bin/python
#-*- coding: utf-8 -*-
import urllib
from xml.dom.minidom import parseString
import sys
##from BeautifulSoup import BeautifulSoup
##from xml.etree.ElementTree import ElementTree
##import nltk
##import lxml.html
import re

def Start(completeUri,count):
    global num
    f=urllib.urlopen(completeUri)
    try:
        data =f.read()#convert to string
        unicode_str=data.decode('utf-8')
        encoded_str=unicode_str.encode('utf-8')
    except TypeError:
        print("error")
    f.close()
    dom =parseString(data)
    ImageParse(dom,count)

def ImageParse(dom,count):
    global num
    print "START {0}\n".format(num)
    imageTitles=dom.getElementsByTagName("mms:Title")
    #print len(imageTitles)
    images=dom.getElementsByTagName("mms:Thumbnail")
    webUrls=dom.getElementsByTagName("mms:DisplayUrl")
    for imageTitle, webUrl,image in zip(imageTitles,webUrls,images):
        imageTitleData=imageTitle.toxml('utf-8').replace('<mms:Title>','').replace('</mms:Title>','')
        webUrlData=webUrl.toxml('utf-8').replace('<mms:DisplayUrl>','').replace('</mms:DisplayUrl>','')
        imageUrl= image.getElementsByTagName("mms:Url")[0]
        imageUrlData=imageUrl.toxml('utf-8').replace('<mms:Url>','').replace('</mms:Url>','').encode('utf-8')
        print "TITLE: {0} \nWEB_URL: {1} \nIMAGE_THUMBNAIL: {2}". format (imageTitleData,webUrlData, imageUrlData)
        count=count+1
        print '\n'
        f=open("SearchData{0}.txt".format(num),"a+")
        f.write("\nTITLE:")
        f.write(imageTitleData)
        f.write("\nIMAGE URL:")
        f.write(imageUrlData)
        f.write("\nWEB URL:")
        f.write(webUrlData)
        f.close()
        WebPageParse(webUrlData,count)
    print"Count",count
    print "END {0}".format(num)
    
def WebPageParse(URL,count):
    global num
    page=urllib.urlopen(URL).read()
    f=open("SearchData{0}.txt".format(num),"a+")
    print "TEXT: "
    f.write("\nTEXT:\n")
    for m in re.finditer("(?#all text)(?s)<(?=[^!--]).+?>.*?(?=<)",page):
            ##print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)|(<script.*)",m.group())
            if(n==None):
                print l.group()
                f.write(l.group().strip())
                f.write("\n")
    f.close()
              

def StreetStyle():
    global num
    url="http://api.bing.net/xml.aspx?Appid={0}&sources={1}&query={2}&{1}.count=1"
    completeUri=url.format('E6C1E113773ED242B82E03F49740BACD17FDAA36','image','globaL street fashion')
    f=open("SearchData{0}.txt".format(num),"w")
    f.write(" ")
    f.close()
    count=0
    Start(completeUri,count)
    ##url="http://api.bing.net/xml.aspx?Appid={0}&sources={1}&query={2}&{1}.count=50&{1}.offset=51"
    ##completeUri=url.format('E6C1E113773ED242B82E03F49740BACD17FDAA36','image','global street fashion')
    ##Start(completeUri,count)

def CelebStreetStyle():
    global num
    num=num+1
    url="http://api.bing.net/xml.aspx?Appid={0}&sources={1}&query={2}&{1}.count=1"
    completeUri=url.format('E6C1E113773ED242B82E03F49740BACD17FDAA36','image','blake lively street style')
    f=open("SearchData{0}.txt".format(num),"w")
    f.write(" ")
    f.close()
    count=0
    Start(completeUri,count)
    ##url="http://api.bing.net/xml.aspx?Appid={0}&sources={1}&query={2}&{1}.count=50&{1}.offset=51"
    ##completeUri=url.format('E6C1E113773ED242B82E03F49740BACD17FDAA36','image','blake lively street style')
    ##Start(completeUri,count)
    
num=3
StreetStyle()
#CelebStreetStyle()




