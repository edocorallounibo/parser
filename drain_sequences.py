#!/usr/bin/env python3
# -*- coding: utf-8 
"""
Created on Fri May 22 17:36:45 2020

@author: edoardo
"""
import configparser
import json
import logging
import sys
import argparse
import pandas as pd
import re

from drain3 import TemplateMiner
from drain3.file_persistence import FilePersistence
from drain3.kafka_persistence import KafkaPersistence

parser=argparse.ArgumentParser(prog='drain_sequences')
group=parser.add_mutually_exclusive_group()
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
args=parser.parse_args()
log_file=args.log_file
if args.frontend:
        log_type="storm-frontend"
        #input_dir = 'frontend-server/'
else:
        log_type="storm-backend"
        #input_dir = 'backend-server/'


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
comp_clustid={}
comp_clustid_abnormal={}
for i in content.index:
    result = template_miner.add_log_message(content[i])
    clustid=re.sub(r'A0*','',result["cluster_id"])
    if comp[i] not in comp_clustid.keys():
        comp_clustid[str(comp[i])]=[str(clustid)]
    else:
        comp_clustid[str(comp[i])].append(str(clustid))
for i in comp.index:
    if level[i]=="ERROR":
        if comp[i] in comp_clustid:
            comp_clustid_abnormal[str(comp[i])]=comp_clustid[str(comp[i])]
            del comp_clustid[str(comp[i])]

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
    if (len(comp_clustid[x])>=10):
         for i in range(len(comp_clustid[x])): 
              normal.write(str(comp_clustid[x][i]))
              normal.write(" ")
         normal.write("\n")
normal.close()
    
