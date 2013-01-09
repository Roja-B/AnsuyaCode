f=open("/media/data3/links1.txt","r")
l=set()
for line in f:
    l.add(line)
f.close()
print len(l)
count=0
for entry in l:
    linkId=entry[:7]
    g=open("/media/netdisk/mallet-2.0.7/ansuya/balatarin/{0}.txt".format(linkId),"w")
    g.write(entry[10:])
    g.close()
    count+=1
print count
