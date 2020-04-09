#!/usr/bin/env python
import sys
sys.path.append('../')
import argparse
import pandas as pd
from logparser import Spell
#from logparser import AEL
#from logparser import Drain
#from logparser import IPLoM
#from logparser import LFA
#from logparser import LenMa
#from logparser import LKE
#from logparser import LogCluster <--no
#from logparser import LogMine <--no
#from logparser import MoLFI
#from logparser import LogSig
#from logparser import SHISO
#from logparser import SLCT

#CLI
parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
group.add_argument("-f","--frontend",action="store_true",help="Used if you want to parse a storm-frontend log file.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
parser.add_argument("log_file",type=str,help="Name of the file you want to parse.")
args=parser.parse_args()

input_dir = '/home/edoardo/storm-t3'
log_file=args.log_file
if args.frontend:
        print("Parsing {} as a frontend log file..".format(log_file))
        log_format = '<Date> <Time> <Pid> - <Level> <Component>: <Content>'#Frontend logformat
elif args.backend:
        print("Parsing {} as a backend log file..".format(log_file))
        log_format = '<Time> - <Level> <Component> - <Content>'#Backend logformat
else:
     	log_format=input("Please, specify a log format:\n")

#Spell----------------------------------------------------
tau        = 0.5  # Message type threshold (default: 0.5)
regex_Spell	 = []  # Regular expression list for optional preprocessing (default: [])
output_dir_Spell = 'Spell_result/'  # The output directory of parsing results from Spell
#AEL------------------------------------------------------
minEventCount = 2 # The minimum number of events in a bin
merge_percent = 0.5 # The percentage of different tokens
regex_AEL     = [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'] # Regular expression list for optional preprocessing (default: [])
output_dir_AEL    = 'AEL_result/' # The output directory of parsing results from AEL
#Drain-----------------------------------------------------
regex_Drain   = [
    r'blk_(|-)[0-9]+' , # block id
    r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)', # IP
    r'(?<=[^A-Za-z0-9])(\-?\+?\d+)(?=[^A-Za-z0-9])|[0-9]+$', # Numbers
]
st         = 0.5  # Similarity threshold
depth	   = 4  # Depth of all leaf nodes
output_dir_Drain = 'Drain_result/'  # The output directory of parsing results from Drain
#IPLoM-----------------------------------------------------
maxEventLen  = 200  # The maximal token number of log messages (default: 200)
step2Support = 0  # The minimal support for creating a new partition (default: 0)
CT           = 0.35  # The cluster goodness threshold (default: 0.35)
lowerBound   = 0.25  # The lower bound distance (default: 0.25)
upperBound   = 0.9  # The upper bound distance (default: 0.9)
regex_IPLoM  = []  # Regular expression list for optional preprocessing (default: [])
output_dir_IPLoM   = 'IPLoM_result/'  # The output directory of parsing results
#LFA-------------------------------------------------------
regex_LFA    = [] # Regular expression list for optional preprocessing (default: [])
output_dir_LFA = 'LFA_result/' # The output directory of parsing results
#LenMa-----------------------------------------------------
threshold  = 0.9 # TODO description (default: 0.9)
regex_LenMa = [] # Regular expression list for optional preprocessing (default: [])
output_dir_LenMa = 'LenMa_result/'# The output directory of parsing results from LenMa
#LKE-------------------------------------------------------
regex_LKE        = [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'] # Regular expression list for optional preprocessing (default: [])
split_threshold  = 3 # The threshold used to determine group splitting (default: 4)
output_dir_LKE   = 'LKE_result/' # The output directory of parsing results
#LogCluster------------------------------------------------
rsupport   = 10 # The minimum threshold of relative support, 10 denotes 10%
regex_LC      = [] # Regular expression list for optional preprocessing (default: [])
output_dir_LC = 'LogCluster_result/' # The output directory of parsing results
#LogMine---------------------------------------------------
levels     = 2 # The levels of hierarchy of patterns
max_dist   = 0.001 # The maximum distance between any log message in a cluster and the cluster representative
k          = 1 # The message distance weight (default: 1)
regex_LM      = []  # Regular expression list for optional preprocessing (default: [])
output_dir_LM = 'LogMine_result/' # The output directory of parsing results
#MoLFI-----------------------------------------------------
regex_MoLFI	 = [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'] # Regular expression list for optional preprocessing (default: [])
output_dir_MoLFI = 'MoLFI_result/'#The output directory of parsing results from MoLFI
#LogSig----------------------------------------------------
regex_LogSig     = []  # Regular expression list for optional preprocessing (default: [])
group_number = 14 # The number of message groups to partition
#SHISO------------------------------------------------------
regex_SHISO	  = [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'] # Regular expression list for optional preprocessing (default: [])
maxChildNum = 4 # The maximum number of children for each internal node
mergeThreshold = 0.1 # Threshold for searching the most similar template in the children
formatLookupThreshold = 0.3 # Lowerbound to find the most similar node to adjust
superFormatThreshold  = 0.85 # Threshold of average LCS length, determing whether or not to create a super format
output_dir_SHISO  = 'SHISO_result/' # The output directory of parsing results
#SLCT-------------------------------------------------------
support    = 10  # The minimum support threshold
regex_SLCT	= []  # Regular expression list for optional preprocessing (default: [])
output_dir_SLCT = 'SLCT_result/'  # The output directory of parsing results

#Manca logmatch
#Gli import commentati danno errore tipo :from logparser import LFA
#  File "../logparser/LFA/__init__.py", line 1, in <module>
#    from LFA import *
#ModuleNotFoundError: No module named 'LFA'
#Oggetti LogParser:

##parser_AEL = AEL.LogParser(input_dir, output_dir_AEL, log_format, rex=regex_AEL, minEventCount=minEventCount, merge_percent=merge_percent)


parser_Spell = Spell.LogParser(indir=input_dir, outdir=output_dir_Spell, log_format=log_format, tau=tau, rex=regex_Spell)


##parser_Drain = Drain.LogParser(log_format, indir=input_dir, outdir=output_dir_Drain,  depth=depth, st=st, rex=regex_Drain)


#parser_IPLoM = IPLoM.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir_IPLoM, maxEventLen=maxEventLen, step2Support=step2Support, CT=CT, lowerBound=lowerBound, upperBound=upperBound, rex=regex_IPLoM)


#parser_LFA = LFA.LogParser(input_dir, output_dir_LFA, log_format, rex=regex_LFA)


#parser_LenMa = LenMa.LogParser(input_dir, output_dir_LenMa, log_format, threshold=threshold, rex=regex_LenMa)


#parser_LKE = LKE.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir_LKE, rex=regex_LKE, split_threshold=split_threshold)

#parser_LC = LogCluster.LogParser(input_dir, log_format, output_dir_LC, rex= regex_LC, rsupport=rsupport)


#parser_LM = LogMine.LogParser(input_dir, output_dir_LM, log_format, rex=regex_LM, levels=levels, max_dist=max_dist, k=k)


##parser_MoLFI = MoLFI.LogParser(input_dir, output_dir_MoLFI, log_format, rex=regex_MoLFI)



#parser_LogSig = LogSig.LogParser(input_dir, output_dir_LogSig, group_number, log_format, rex=regex_LogSig)


#parser_SHISO = SHISO.LogParser(log_format,indir=input_dir,outdir=output_dir_SHISO, rex=regex_SHISO, maxChildNum=maxChildNum, mergeThreshold=mergeThreshold, formatLookupThreshold=formatLookupThreshold, s$

#parser_SLCT = SLCT.LogParser(log_format=log_format, indir=input_dir, outdir=output_dir_SLCT, support=support, rex=regex_SLCT)

#parser_AEL.parse(log_file)
parser_Spell.parse(log_file)
#parser_Drain.parse(log_file)
#parser_IPLoM.parse(log_file)
#parser_LFA.parse(log_file)
#parser_LenMa.parse(log_file)
#parser_LKE.parse(log_file)
#parser_LC.parse(log_file)
#parser_LM.parse(log_file)
##parser_MoLFI.parse(log_file)
#parser_LogSig.parse(log_file)

#CONVERSION TO SEQUENCES
df = pd.read_csv("/cont/logparser/parser/Spell_result/{}_structured.csv".format(log_file))#
if args.frontend:
    eid = df.loc[:,"EventId"]
    comp = df.loc[:,"Component"]
    pid = df.loc[:,"Pid"]
    level=df.loc[:,"Level"]
    seen_event = set()
    uniq_event = []
    #Translates Event_id's hex to integer depending on the order of appearance
    for x in eid:
        if x not in seen_event:
            uniq_event.append(x)
            seen_event.add(x)
    event_dict = {uniq_event[i] : i+1  for i in range (0,len(uniq_event))}

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
    file=open("/cont/DeepLog_no_tensorboard/data/{}_train".format(log_file),"w")
    for x in comp_eid.keys():
        if (len(comp_eid[x])>=10):
            for i in range(len(comp_eid[x])): 
                file.write(str(comp_eid[x][i]))
                file.write(" ")
            file.write("\n")
    file.close()

    file=open("/cont/DeepLog_no_tensorboard/data/{}_abonormal".format(log_file),"w")
    for x in abnormal.keys():
        for i in range(len(abnormal[x])):
            file.write(str(abnormal[x][i]))
            file.write(" ")
    file.write("\n")
    
else:
    print("WIP")    
