#!/usr/bin/env python3
# -*- coding: utf-8 
"""
Description : Example of using Drain3 with Kafka persistence
Author      : David Ohana, Moshik Hershcovitch, Eran Raichstein
Author_email: david.ohana@ibm.com, moshikh@il.ibm.com, eranra@il.ibm.com
License     : MIT
"""
import configparser
import json
import logging
import sys
sys.path.append('../')
import argparse
import pandas as pd
import importlib
importlib.import_module('drain3')

from drain3 import TemplateMiner
from drain3.file_persistence import FilePersistence
from drain3.kafka_persistence import KafkaPersistence


parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
args=parser.parse_args()
log_file=args.log_file
if args.frontend:
        log_type="frontend-server"
        input_dir = '/container/drain3/parser/results/frontend-server'
        log_format = '<Date> <Time> <Pid> - <Level> <Component>: <Content>'#Frontend logformat
        print("Parsing {} with [{}] format".format(log_file,log_format))
        
elif args.backend:
        log_type="backend-server"
        input_dir = '/container/drain3/parser/results/backend-server/'
        log_format = '<Time> - <Level> <Component> - <Content>'#Backend logformat
        print("Parsing {} with [{}] format".format(log_file,log_format))
        

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
print(f"Drain3 started with '{persistence_type}' persistence")

df = pd.read_csv("/container/drain3/parser/results/{}/{}_struct.csv".format(log_type,log_file))#
content=df.loc[:,'Content']

for idx in content.index:
        #component=line['Component']
        #level=line['Level']
        result=template_miner.add_log_message(content[idx])
        result_json = json.dumps(result)
        print(result_json)
        #result_json=json.dump(result)
        
print("Clusters:")
for cluster in template_miner.drain.clusters:
    print(cluster)
