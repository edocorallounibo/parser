import pandas as pd
import pickle
import os
import argparse


parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
args=parser.parse_args()

#input_dir = '../logfiles/'
log_file=args.log_file
if args.frontend:
        log_type="storm-frontend"
elif args.backend:
        log_type="storm-backend"
else:
        log_type=input("Specify log_type:")

#CONVERSION TO SEQUENCES

df = pd.read_csv("/container/logparser/parser/Spell_result/{}_structured.csv".format(log_file))#
eid = df.loc[:,"EventId"]
comp = df.loc[:,"Component"]
pid = df.loc[:,"Pid"]
level=df.loc[:,"Level"]
if os.path.isfile("/home/edocorallo/logfiles/frontend-server/{}_uniq_event.pickle".format(log_type)):
    file_in=open("/home/edocorallo/logfiles/frontend-server/{}_uniq_event.pickle".format(log_type),"rb")
    uniq_event=pickle.load(file_in)
    file_in.close()
else
    uniq_event = []
#Translates Event_id's hex to integer depending on the order of appearance
for x in eid:
    if x not in uniq_event:
        uniq_event.append(x)
event_dict = {uniq_event[i] : i+1  for i in range (0,len(uniq_event))
file_out=open("/home/edocorallo/logfiles/frontend-server/{}_uniq_event.pickle".format(log_type),"wb")
pickle.dump(uniq_event,file_out)
file_out.close()
comp_eid={}
abnormal={}
#Associates components(?)(like '[9d58ad19-c19c-457d-b5eb-18ead4c239b0]') to all message types in event_dict
for i in comp.index:
   if comp[i] not in comp_eid.keys():
        comp_eid[comp[i]]=[event_dict.get(eid[i])]
   else:
        comp_eid[comp[i]].append((event_dict.get(eid[i])))

for i in level.index:
   if level[i]=="ERROR":
      if comp[i] in comp_eid:
        abnormal[comp[i]]=comp_eid[comp[i]]
        del comp_eid[comp[i]]
file=open("/container/DeepLog_no_tensorboard/data/{}_normal".format(log_file),"w")
for x in comp_eid.keys():
    if (len(comp_eid[x])>=10):
         for i in range(len(comp_eid[x])): 
            file.write(str(comp_eid[x][i]))
            file.write(" ")
         file.write("\n")
file.close()

file=open("/container/DeepLog_no_tensorboard/data/{}_abonormal".format(log_file),"w")
for x in abnormal.keys():
    for i in range(len(abnormal[x])):
        file.write(str(abnormal[x][i]))
        file.write(" ")
    file.write("\n")
file.close()   
