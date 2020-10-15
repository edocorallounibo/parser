#!/usr/bin/env python3
# -*- coding: utf-8 
"""
Author      : edocorallounibo
Author_email: edoardo.corallo@gmail.com
License     : MIT
"""
import configparser
import json
import logging
import sys
import argparse
import pandas as pd
import re
from datetime import datetime as dt
from drain3 import TemplateMiner
from drain3.file_persistence import FilePersistence
from drain3.kafka_persistence import KafkaPersistence


parser=argparse.ArgumentParser(prog='drain_sequences')
group=parser.add_mutually_exclusive_group()
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
parser.add_argument("-window_size",default=10,type=int,help="Sequences will be at least (window_size)+1 long")
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
args=parser.parse_args()
log_file=args.log_file
if args.frontend:
        log_type="frontend-server"
elif args.backend:
        log_type="backend-server"
else:
        print("this line is never printed and thus useless!")

# persistence_type = "NONE"
# persistence_type = "KAFKA"
persistence_type = "FILE"

config = configparser.ConfigParser()
config.read('drain3.ini')

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(message)s')

if persistence_type == "KAFKA":
    persistence = KafkaPersistence("localhost:9092", "drain3_state")
elif persistence_type == "FILE":
    persistence = FilePersistence("results/{}/drain3_state[{}].bin".format(log_type,log_type))
else:
    persistence = None
template_miner = TemplateMiner(persistence)
df=pd.read_csv("results/{}/{}_struct.csv".format(log_type,log_file))
comp=df.loc[:,"Component"]
content=df.loc[:,"Content"]
level=df.loc[:,"Level"]
time=df.loc[:,"Time"]
comp_clustid={}
comp_time={}
comp_clustid_abnormal={}
comp_time_abnormal={}
fail_pattern=re.compile(r'FAILURE')
error_pattern=re.compile(r'ERROR')
for i in content.index:
    result = template_miner.add_log_message(content[i])
    clustid=re.sub(r'A0*','',result["cluster_id"])
    if comp[i] not in comp_clustid.keys():
        comp_clustid[str(comp[i])]=[str(clustid)]
       
    else:
        comp_clustid[str(comp[i])].append(str(clustid))
        
for i in time.index:
        if comp[i] not in comp_time.keys():
            comp_time[str(comp[i])]=[str(time[i])]
        else:
            comp_time[str(comp[i])].append(str(time[i]))
for x in comp_time.keys():
    for i in range(len(comp_time[x])):
        i+=1
        if i<len(comp_time[x]):
            comp_time[x][-i]=str((dt.strptime(comp_time[x][-i],'%H:%M:%S.%f')-dt.strptime(comp_time[x][-(i+1)],'%H:%M:%S.%f')).total_seconds())
        else:
            comp_time[x][0]='0'
for i in comp.index:
    match_error=re.search(error_pattern,content[i])
    match_failure=re.search(fail_pattern,content[i])
    if match_error or match_failure:
        if comp[i] in comp_clustid:
            comp_clustid_abnormal[str(comp[i])]=comp_clustid[str(comp[i])]
            comp_time_abnormal[str(comp[i])]=comp_time[str(comp[i])]
            del comp_clustid[str(comp[i])]
            del comp_time[str(comp[i])]

abnormal=open("results/{}/{}_abnormal".format(log_type,log_file),"w")
for x in comp_clustid_abnormal.keys():
    #if (len(comp_clustid[x])>=10):
         for i in range(len(comp_clustid_abnormal[x])): 
              abnormal.write(str(comp_clustid_abnormal[x][i]))
              abnormal.write(" ")
         abnormal.write("\n")
abnormal.close()
normal=open("results/{}/{}_normal".format(log_type,log_file),"w")
for x in comp_clustid.keys():
    if (len(comp_clustid[x])>args.window_size):
         for i in range(len(comp_clustid[x])): 
              normal.write(str(comp_clustid[x][i]))
              normal.write(" ")
         normal.write("\n")
normal.close()
abnormal=open("results/{}/{}_timestamps_abnormal".format(log_type,log_file),"w")
for x in comp_time.keys():
         for i in range(len(comp_time[x])): 
              abnormal.write(str(comp_time[x][i]))
              abnormal.write(" ")
         abnormal.write("\n")
abnormal.close()
normal=open("results/{}/{}_timestamps_normal".format(log_type,log_file),"w")
for x in comp_time.keys():
    if (len(comp_time[x])>args.window_size):
         for i in range(len(comp_time[x])): 
              normal.write(str(comp_time[x][i]))
              normal.write(" ")
         normal.write("\n")
normal.close()   
