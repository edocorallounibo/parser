#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 14:04:15 2020

@author: edoardo
"""
import argparse

parser=argparse.ArgumentParser()
group=parser.add_mutually_exclusive_group()
parser.add_argument("file",type=str,help="Name of the file you want to parse.")
group.add_argument("-b","--backend",action="store_true",help="Used if you want to parse a storm-backend log file.")
args=parser.parse_args()
file=args.file
if args.backend:
        log_type="backend-server"
else:
        log_type="frontend-server"

text = "results/{}/{}".format(log_type,args.file)
file_in=open(text,'r')
file_out=open("results/{}/post_{}".format(log_type,args.file),'w')
post_proc_dict={"13":"1",#process_request : Connection from <IP>
                "37":"4",#ns1__srmLs : Request: Ls. IP: <IP>. Client DN: <ID>  
                "8":"5",#Request <TSK> from Client IP='<IP>' Client DN=<ID># Requested token '<TKN>' on <NUM> SURL(s): '<URL>
                "10":"5",
                "19":"5",
                "33":"5",
                "38":"5",
                "39":"5",
                "45":"5",
                "46":"5",
                "47":"5",
                "49":"5",
                "60":"5",
                "61":"5",
                "62":"5",
                "63":"5",
                "64":"5",
                "65":"5",
                "81":"5",
                "36":"7",#Result for request <TSK> is 'SRM_REQUEST_INPROGRESS'
                "14":"9",# Request <TSK> from Client IP='<IP>' Client DN=<ID># Requested <NUM> SURL(s): '<URL>
                "29":"15",#ns1__srmReleaseFiles : Request: Release files. IP: <IP>. Client DN: <ID>(s): <URL> token: <TKN>
                "40":"15",
                "25":"17",#__process_file_request<> : Received - <*> - protocols, <*> are supported, <*> are not supported
                "42":"17",
                "48":"31",#ns1__srmAbortFiles : Request: Abort files. IP: <IP>. Client DN: <ID>(s): <URL> token: <TKN>
                "50":"31",
                "51":"31",
                "52":"31",
                "53":"31",
                "54":"31",
                "58":"31",
                "67":"31",
                "68":"31",
                "56":"55",#rpcResponseHandler_Ls : ERROR: XML-RPC Fault: RPC failed at server. Failed to invoke method ls in class...
                "69":"55",
                "70":"55",               
                }

for line in file_in:
    for f_key in post_proc_dict.keys():
        if f_key in line:
            line = line.replace(f_key,post_proc_dict[f_key])
    file_out.write(line)        
file_in.close()
file_out.close()
