#!/usr/local/bin/python

# This program reads data collected from mothering.com and enters it in MongoDB database called Mothering. 

# Author:Roja Bandari and Ansuya
# March 2012

from pymongo import Connection
connection = Connection()
motheringdb = connection.Mothering
threads = motheringdb.threads

log = open("mongoError.log","a")
f=open("/home/ansuya/Vaccination_Data/ViewsNPostsMothering.txt","r")
i = 0
for line in f:
     i+=1
     if(i>1):
         tag = (line.split(':')[0])
         value= (line.split(':')[1]).strip()
         if tag =="THREAD_ID": thread_id = value
         elif tag =="VIEWS": views = value              
         elif tag =="NO. OF POSTS": 
            thread_length = value
            new_record = [{"threadId" : thread_id, "views": views, "threadLength":thread_length}]
            threads.insert(new_record)
                #print i
     #     print new_record
#     except:
#          log.write(line)
#          continue
     

print "Total entries processed = " + str(i)
f.close()
log.close()

