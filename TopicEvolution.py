
def maxtopicprop(f):
    count=0
    threadtopicprops=[]
    
    for line in f:
        count+=1
        print count
        if count>1:
            topicprops={}
            l=line.split('\t')
            threadId=l[1].split('/')[6].split('.')[0]
            i=3
            while i<13: #23:
                topicprops[l[i-1]]=float(l[i])
                i+=2
            tp=[]
            for key in sorted(topicprops.iterkeys()):
                tp.append(topicprops[key])
            threadtopicprops.append([threadId,tp]) 
    return threadtopicprops          

tops=[0,8,9,3,5,7,1]
for top in tops :
    f=open('/media/netdisk/ansuya/mallet-2.0.7/cafemomthreadtopic{0}doctopics1'.format(top),'r')#cafemomthread1doctopics','r')
    ttp=maxtopicprop(f)
    f.close()
    f=open("/media/netdisk/ansuya/cafemomwork/CafemomTimeSlots.txt","r")#time_cluster threadId userId postId date
    g=open("/media/netdisk/ansuya/AvgTopicStrengthtopic{0}.txt".format(top),"w")#AvgTopicStrength1.txt","w")
    slots=[]
    l=0
    sloti=1
    for line in f:
        yes=0
        timeSlot=line.split("\t")[0]
        if l==0:
            prevTimeSlot=timeSlot
            slot=[0.0,0.0,0.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0]
        threadId=line.split("\t")[1]#.split("\n")[0]
        for entry in ttp:
            if threadId==entry[0]:
                tp=entry[1]
                yes=1
                break
            else: yes=0
        if timeSlot!=prevTimeSlot:
            temp=[]
	    #print "Slot", prevTimeSlot
            for entry in slot:
                temp.append(entry/sloti)
	        #print "No. of threads in this slot", sloti
            slot=[]
            slot=temp
            slots.append(slot)
            sloti=1
            slot=[0.0,0.0,0.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0]
        if yes==1:
            temp=[]
            for a,b in zip(slot,tp):
                temp.append(a+b)
            slot=[]
            slot=temp 
            sloti+=1   
        prevTimeSlot=timeSlot
        l+=1
        print l
        #g.write(str(l))
        #g.write("\n")
    temp=[]
    for entry in slot:
        temp.append(entry/sloti)
    slot=[]
    slot=temp
    slots.append(slot)

    #print slots
    i=0
    for entry in slots:
        #g.write(str(i))
        #g.write("\t")
        for prop in entry:
	    g.write(str(prop))
            g.write("\t")
        g.write("\n")
        i+=1
    g.close()
    f.close()
