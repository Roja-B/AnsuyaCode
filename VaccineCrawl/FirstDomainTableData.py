from __future__ import with_statement
from urlparse import urlparse
import re
from collections import Counter
import pickle 
import xlwt

def Start():
    f=open("Vaccination_Data/ViewsNPostsMothering1.txt","r").read()
    thr_pos=re.findall("(?s)THREAD_ID: ([^A-Za-z]+?)\\nFIRST POST CONTAINS LINK: 1\\nNO. OF POSTS: (.+?)\\n",f)
    #print len(thr_pos)
    f=open("UserFirstLinksMothering.txt","r").read()
    thr_usr_l=re.findall("(?s)THREAD_ID: (.+?)\\nUSER_ID: .+?\\nLINKS: (.+?)\\n",f)
    #print len(thr_usr_l)
    l=[]
    for i in range(len(thr_usr_l)):
        thr_id=[]
        thr_id.append(thr_usr_l[i][0])
        links_thread=re.findall("(?<=\\s).+?(?=\\s)",thr_usr_l[i][1])
        for j in range(len(thr_pos)):
            if(thr_usr_l[i][0]==thr_pos[j][0]):
                no_posts=[]
                no_posts.append(thr_pos[j][1])
        while(links_thread):
            l.append((links_thread.pop(),thr_id,no_posts))

    d=sorted(l)
    i=0
    j=i+1
    while(i!=len(d)-1):
        ##print "i=", i
        ##print "j=", j
        if(d[i][0]==d[j][0]):
            d[i][1].extend(d[j][1])
            d[i][2].extend(d[j][2])
            del d[j]
            ##print d
        else:
            i=i+1
            j=i+1
    print len(d)
    f=open("DomainTable.txt","w") 
    for item in d:
        f.write("\nDOMAIN: ")
        f.write(item[0])
        while(item[1] and item[2]):
            f.write("\nTHREAD_ID: ")
            f.write(item[1].pop())
            f.write("\nNO. OF POSTS: ")
            f.write(item[2].pop())
            
    f.close()
         
Start()   
