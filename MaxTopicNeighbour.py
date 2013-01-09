f=open("/media/netdisk/ansuya/mallet-2.0.7/cafemomthread1doctopics","r")
i=0
j=0
count=0
for line in f:
    if count!=0:
        tp1=line.split("\t")[3]
	if float(tp1)>=0.4:
            tp2=line.split("\t")[5]
            l=5
            while float(tp1) == float(tp2) and l<23:
   	        tp2=line.split("\t")[l]
	        l+=2
            #if float(tp1) - float(tp2) <= 0.05:
	    #    i+=1
            if float(tp1) - float(tp2) <= 0.2:
	        j+=1
    count+=1
    print count
print i, j	
