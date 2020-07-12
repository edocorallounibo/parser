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
import os
import argparse
import re
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
        log_type="storm-frontend"
        input_dir = '/container/logfiles/frontend-server/'
        print("Parsing {} as a frontend log file..".format(log_file))
        log_format = '<Date> <Time> <Pid> - <Level> <Component>: <Content>'#Frontend logformat
elif args.backend:
        log_type="storm-backend"
        input_dir = '/container/logfiles/backend-server/'
        print("Parsing {} as a backend log file..".format(log_file))
        log_format = '<Time> - <Level> <Component> - <Content>'#Backend logformat
try:
    os.mkdir("results")
except OSError:
    pass
else:
    print("results directory created")
try:
    os.mkdir("results/{}".format(log_type))
except OSError:
    pass
else:
    print("{} directory made".format(log_type))
    
################
def load_data():
        headers, regex =generate_logformat_regex(log_format)
        return log_to_dataframe(os.path.join(input_dir, log_file), regex, headers, log_format)

def log_to_dataframe(logfile, regex, headers, logformat):
        """ Function to transform log file to dataframe 
        """
        log_messages = []
        linecount = 0
        with open(logfile, 'r') as fin:
            for line in fin.readlines():
                line = re.sub(r'[^\x00-\x7F]+', '<NASCII>', line)
                try:
                    match = regex.search(line.strip())
                    message = [match.group(header) for header in headers]
                    log_messages.append(message)
                    linecount += 1
                except Exception as e:
                    pass
        logdf = pd.DataFrame(log_messages, columns=headers)
        logdf.insert(0, 'LineId', None)
        logdf['LineId'] = [i + 1 for i in range(linecount)]
        if os.path.isfile("results/{}/{}_struct.csv".format(log_type,log_file)):
            pass
        else:
            file_out=open("results/{}/{}_struct.csv".format(log_type,log_file),"w")
            logdf.to_csv(file_out)
            file_out.close()
        return logdf
def generate_logformat_regex(logformat):
        """ Function to generate regular expression to split log messages
        """
        headers = []
        splitters = re.split(r'(<[^<>]+>)', logformat)
        regex = ''
        for k in range(len(splitters)):
            if k % 2 == 0:
                splitter = re.sub(' +', '\s+', splitters[k])
                regex += splitter
            else:
                header = splitters[k].strip('<').strip('>')
                regex += '(?P<%s>.*?)' % header
                headers.append(header)
        regex = re.compile('^' + regex + '$')
        return headers, regex
################





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



for idx, line in load_data().iterrows():
        #component=line['Component']
        #level=line['Level']
        result=template_miner.add_log_message(str(line['Content']))
        result_json = json.dumps(result)
        print(result_json)
        #result_json=json.dump(result)
        
print("Clusters:")
for cluster in template_miner.drain.clusters:
    print(cluster)
