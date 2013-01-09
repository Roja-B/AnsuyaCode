
f=open("/media/data3/roja/forAnsuya/links.txt","r")
g=open("/media/data3/roja/forAnsuya/politics_linkIds.txt","r")
h=open("/media/data3/links1.txt","a")

links=[]
for line in g:
    links.append(line.strip())

print "Links to be included", len(links), "eg", links[0]

g.close()
balatarin=[]# consisting of a 2 item tuple; 0->number , 1->text
count=0
linkId=''
text=''
title=''
start= True
line_no=1
entry=[]
for line in f:
    print "line number", line_no
    line=line.strip()
    link_id=line[:7]
    if(link_id.isdigit()==True):
        if(start==False):
            if(text[:10]!='###DONT###'):
                entry=[]
                entry.append(linkId)
                entry.append(text)
                balatarin.append(entry)
                print "Entry added"
                count+=1
        if(link_id in links):
            linkId=link_id
            try:
                title=line.split('\t')[1]
            except IndexError:
                title=''
            title=title+'.'
            #print title
            try:
                text=line.split('\t')[2]
            except IndexError:
                text=''
            #print text
            text=title+' '+text
        else:
            print "Not to be included"
            linkId=link_id
            title=''
            text='###DONT###'
        start=False
    else:
        text=text+' '+line
        text=text.strip()
        print "Appending"
    line_no+=1    
    #break
    
if(text[:10]!='###DONT###'):
    entry=[]
    entry.append(linkId)
    entry.append(text)
    balatarin.append(entry)
    print "Entry added"
    count+=1
    
balatarin=sorted(balatarin)
i=0
j=i+1
while(i!=len(balatarin)-1):
    ##print "i=", i
    ##print "j=", j
    if(balatarin[i][0]==balatarin[j][0]):
        balatarin[i][1]+=(' '+balatarin[j][1])
        del balatarin[j]
        ##print d
    else:
        i=i+1
        j=i+1
        
for entry in balatarin:
    h.write(entry[0])
    h.write(' ')
    h.write('_')
    h.write(' ')
    h.write(entry[1])
    h.write('\n')
    print "Entry written to file"
print count, len(links), len(balatarin)
#print balatarin
h.close()
f.close()
