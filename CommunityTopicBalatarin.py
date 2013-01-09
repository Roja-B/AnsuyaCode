#To find relevant topics for each community
#Output-> TIME<tab>COMMUNITY<tab>TOPIC[<comma>TOPIC]<colon>PROPORTION<tab>....<newline>
#By Ansuya Ahluwalia 05-07-2012

#Extract topic and proportions for all links and store in list 'toprop'
f=open("/media/netdisk/mallet-2.0.7/maxtopicprop.txt","r")
toprop=[]
for line in f:
    link=line.split("\t")[0]
    topics=line.split("\t")[1]
    prop=line.split("\t")[2].replace("\n","")
    toprop.append((link,(topics,prop)))
toprop=dict(toprop)
f.close()

#Create output file
g=open("/media/data3/roja/forAnsuya/CommunityTopicBalatarin.txt","w")

#Extract time from file below to create folder names for each timeline and store in list 'time'
f=open("/media/data3/roja/forAnsuya/U-pol_J100VT5_stats_combined.txt","r")
time=set()
for line in f:
    time.add("1005"+line.split(" ")[0].replace("-",""))
time=list(time)
f.close()
count=0

#Open specific repLinks.txt file for each time folder 
for entry in time:
    #Mention the correct path upto time folder name {0} and the following path to repLinks.txt in the line below
    f=open("/media/roja/.../{0}/.../repLinks.txt".format(entry)","r") 
    #f=open("/media/data3/roja/forAnsuya/repLinks.txt","r")
    for line in f:
        #Extract community number from file and write to output file
        if(line[:3]=="***"):
            community=line.split(" ")[2].replace("\n","")
            g.write("\n")
            g.write(entry)
            g.write('\t')
            g.write(community)
            g.write('\t')
            count+=1
        else:
            #Find each linkId for each community, in the 'toprop' list containing linkId, topic and proportions and write to output file
            topicp= [toprop[key] for key in toprop.keys() if line.split(" ")[1] in key]
            print topicp
            g.write(topicp[0][0])
            g.write(':')
            g.write(topicp[0][1])
            g.write("\t")
    f.close()
print "Total communities in all timelines", count 
g.close()
