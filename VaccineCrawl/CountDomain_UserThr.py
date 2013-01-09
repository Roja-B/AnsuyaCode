from __future__ import with_statement
from urlparse import urlparse
import re
from collections import Counter
import pickle 
import xlwt



def getDomain(url, tlds):
    try:
        
        urlElements = urlparse(url)[1].split('.')
        # urlElements = ["abcde","co","uk"]

        for i in range(-len(urlElements),0):
            lastIElements = urlElements[i:]
            #    i=-3: ["abcde","co","uk"]
            #    i=-2: ["co","uk"]
            #    i=-1: ["uk"] etc

            candidate = ".".join(lastIElements) # abcde.co.uk, co.uk, uk
            wildcardCandidate = ".".join(["*"]+lastIElements[1:]) # *.co.uk, *.uk, *
            exceptionCandidate = "!"+candidate

            # match tlds: 
            if (exceptionCandidate in tlds):
                return ".".join(urlElements[i:]) 
            if (candidate in tlds or wildcardCandidate in tlds):
                return ".".join(urlElements[i-1:])
                # returns "abcde.co.uk"
    except (ValueError):
        pass
        
def start():
    f=open("Vaccination_Data/ViewsNPostsMothering1.txt","r").read()
    thr_pos=re.findall("(?s)THREAD_ID: ([^A-Za-z]+?)\\nFIRST POST CONTAINS LINK: 1\\nNO. OF POSTS: (.+?)\\n",f)
    #print len(thr_pos)
    f=open("UserFirstLinksMothering.txt","r").read()
    thr_usr_l=re.findall("(?s)THREAD_ID: (.+?)\\nUSER_ID: (.+?)\\nLINKS: (.+?)\\n",f)
    #print len(thr_usr_l)
    
    # load tlds, ignore comments and empty lines:
    with open("effective_tld_names.txt") as tldFile:
        tlds = [line.strip() for line in tldFile if line[0] not in "/\n"]   
    f=open("Vaccination_Data/UserLinksMothering.txt","r").read() 
    blocks=re.findall("(?s)USER_ID.+?LINKS.+?(?=USER)",f)
    u=0
    user_dict=[]
    for block in blocks:  
        u=u+1
        user_id=re.search("(?<=USER_ID: )(.+?)(?=\\s)",block).group()
        domains=re.findall("http://.+?\\s|https://.+?\\s",block)
        count1=0
        DOMAINS=[]
        for domain in domains:
            count1=count1+1
            dom=str(getDomain(domain,tlds))
            if(dom!=None):
                DOMAINS.append(dom)
        ##print count1,DOMAINS
        user_dict.append((user_id,DOMAINS))
    d=sorted(user_dict)
    print "TOTAL POSTS WITH LINKS", u   
    print len(d)
    wbk=xlwt.Workbook()
    sheet=wbk.add_sheet('sheet 1')
    r=1
    sheet.write(0,0,'USER_ID')
    sheet.write(0,1,'DOMAINS MENTIONED')
    sheet.write(0,2,'DOMAIN OCCURRENCE')
    sheet.write(0,3,'TOTAL LINKS')
    sheet.write(0,4,'OCCURS IN THE FIRST POST OF A THREAD')
    sheet.write(0,5,'NO. OF POSTS IN THAT THREAD')
    sheet.write(0,6,'THREAD_ID')
    i=0
    j=i+1
    while(i!=len(d)-1):
        ##print "i=", i
        ## print "j=", j
        if(d[i][0]==d[j][0]):
            d[i][1].extend(d[j][1])
            del d[j]
            ##print d
        else:
            i=i+1
            j=i+1
    print "TOTAL USERS WHO POSTED LINKS", len(d)

    for i in range(len(d)):
        e=Counter(d[i][1])
        ##print e
        s=0
        for key,value in e.iteritems():
            sheet.write(r,0,d[i][0])
            sheet.write(r,1,key)
            sheet.write(r,2,value)
            loop=0
            for j in range(len(thr_usr_l)):
                if(d[i][0]==thr_usr_l[j][1]):
                    #print "user_id",d[i][0], thr_usr_l[j][l], "\n"
                    if(re.search("\\s"+str(key)+"\\s",thr_usr_l[j][2])!=None):
                        loop=loop+1
                        if(loop>=2):
                            r=r+1
                        sheet.write(r,4,'1')
                        #print "domain", key,"\n"
                        for k in range(len(thr_pos)):
                            if(thr_usr_l[j][0]==thr_pos[k][0]):
                                sheet.write(r,5,thr_pos[k][1])
                                sheet.write(r,6,thr_pos[k][0])
                                #print "no. of posts", thr_pos[k][1],"\n"
            s=s+value
            r=r+1
        sheet.write(r-1,3,s)
    wbk.save('UserDomainCount.xls')
    
    sheet=wbk.add_sheet('sheet 2')
    r=1
    sheet.write(0,0,'USER_ID')
    sheet.write(0,1,'DOMAINS MENTIONED')
    sheet.write(0,2,'DOMAIN OCCURRENCE')
    sheet.write(0,3,'COMMUNITY')
    sheet.write(0,4,'TOTAL LINKS')
    n=['121875','48441','1342','6301','77851','12308','13270','22126','26532','131','6972','8568','80061','43983','46781','11963','5796','5654','42','11800']
    c=[1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]
    i=0
    j=i+1
    while(i!=len(d)-1):
        ##print "i=", i
        ## print "j=", j
        if(d[i][0]==d[j][0]):
            d[i][1].extend(d[j][1])
            del d[j]
            ##print d
        else:
            i=i+1
            j=i+1
    print "TOTAL USERS WHO POSTED LINKS", len(d)
    for i in range(len(d)):
        e=Counter(d[i][1])
        ##print e
        s=0
        if(d[i][0] in n):
            x=n.index(d[i][0])
            for key,value in e.iteritems():
                sheet.write(r,0,d[i][0])
                sheet.write(r,1,key)
                sheet.write(r,2,value)
                sheet.write(r,3,c[x])
                s=s+value
                r=r+1
            sheet.write(r-1,4,s)
    wbk.save('UserDomainCount.xls')
    
            
start()
