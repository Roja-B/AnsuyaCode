#from xlrd import open_workbook
import urllib,httplib,re

def readUrls():
    global l
    # Read excel workbook using xlrd. Support for reading .xlsx (Excel 2007) format is not available at the moment
    #wb=open_workbook('/home/ansuya/googleSearchGardasilCervarix.xlsx')
    #for s in wb.sheets():
    #    print 'Sheet : ',s.name
    #    for row in range(s.nrows):
    #        for col in range(s.ncols):
    #            l.append(s.cell(row,col).value)
    
    #Read Excel workbook by unzipping the archive to Xml   
    f=open("/home/ansuya/sharedStrings.xml").read()
    links=re.findall("(?s)<t>(.+?)</t>",f)
    for link in links:
        l.append(link.strip())
    print "Check list- ", l[0], l[99]
    print "Total links ", len(l)
    
count=0
errorcount=0
wcount=0
l=[]
readUrls()
#l=list(set(l))
f=open("/media/netdisk/GardasilCervarix.txt","a")
for entry in l:
    try:
        req=urllib.urlopen(entry)
        page=req.read()
        returnUrl=req.geturl()
        wcount+=1
        if(entry!=returnUrl):
            print entry ,"redirected to", returnUrl
            f.write("\n****google search result****html content download****\n")
            f.write(entry)
            f.write("\n")
            f.write(page)
    except (urllib.HTTPError): # Generates HttpError 403 which indicates that the web server is not giving a reponse for the http request made. Reason unknown.
        print "No response from web server for  ",entry
        errorcount+=1
    count+=1
    print count
print "Error count", errorcount
print "Links visited", wcount
print "Total links", count
f.close()
