#f=open("/media/data3/roja/forAnsuya/linksAndUsers.txt","r")
#g=open("/media/data3/linksAndUsers1.txt","w")
#
#for line in f:
#    g.write(line[:8])
#    g.write("b ")
#    g.write(line[8:])
#
#g.close()
#f.close()

import re

f=open("/media/data3/linksAndUsers1.txt","r")
g=open("/media/data3/linksAndUsers2.txt","w")
for line in f:
    spaces=re.findall(" ",line)
    if(len(spaces)>=6):
        g.write(line)
f.close()
g.close()
