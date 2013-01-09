import re
import urllib

def reg():
    ##f=open("TestHTML.txt","r").read()
    f=urllib.urlopen("http://www.mothering.com/community/t/1346818/exemptions-under-attack").read()
    script=0
    comment=0
    List=regScript()
    List.reverse()
    for m in re.finditer("(?#all text)(?s)<.+?>.*?(?=<)",f):
            ##print"1111: ", m.group(),"\n"
            l=re.search("(?s)(?<=>).*",m.group())
            n=re.search("(?s)(<style.*)",m.group())
            o=re.search("(?s)(<script.*)",m.group())
            p=re.search("(?s)<!--.*?-->.*",m.group())
            p=re.search("(?s)<!--.*",m.group())
            if(p!=None or comment==1):
                comment=1
                check=re.search("(?s).*-->.*",m.group())
                if(check!=None):
                    print "CHECK ",check.group(),"\\CHECK \n"
                    comment=0
                    q=re.search("(?s)(?<=-->).*",check.group())
                    if(q!=None):
                        print q.group().strip()
            if(n==None and o==None and p==None and script!=1 and comment!=1):
                print l.group().strip()
            elif(o!=None or script==1 and over==0):
                over=0
                script=1
                check=re.search("(?s)</script>.*",m.group())
                if(check!=None):
                    script=0
                if(o!=None):
                    if(List):
                        inside_list=List.pop()
                        inside_list.reverse()
                        while(inside_list):
                            print inside_list.pop()
                    else:
                        over=1
                               
def regScript():
    ##f=open("TestHTML.txt","r").read()
    f=urllib.urlopen("http://www.mothering.com/community/t/1346818/exemptions-under-attack").read()
    list_text=[]
    for k in re.finditer("(?#all script tags)(?s)<script.*?>.*?<(?=/script>)",f):
        m=re.search("(?#everything enclosed)(?s)(?<=>).*",k.group())
        each_tag_text=[]
        ##print "1111: ",m.group(),"\n"
        for n in re.finditer("(?#all text)(?s)(?<=>)[^}{]*?(?=<)",m.group()):
            ##print "2222: ",n.group().strip()
            each_tag_text.append(n.group().strip())       
        list_text.append(each_tag_text)
    return list_text
                
reg()
