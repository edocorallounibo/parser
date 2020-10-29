#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:56:43 2020

@author: edoardo
"""
import re
_in=input("input file :")
_out=input("output file :")

d={}
uniq=[]
with open('/container/drain3/parser/results/frontend-server/merged_normal','r') as file:
    for line in file:
        line=line.strip().split()
        for char in line:
            if char!=0 and char not in uniq:
                uniq.append(char)
with open('/container/drain3/parser/results/frontend-server/merged_abnormal','r') as file:
    for line in file:
        line=line.strip().split()
        for char in line:
            if char not in uniq:
                uniq.append(char)
for i in range(0,len(uniq)):
    d[str(uniq[i])]=str(i+1)
fout=open('/container/DeepLog_no_tensorboard/data/{}'.format(_out),'w')
with open('/container/DeepLog_no_tensorboard/data/{}'.format(_in),'r') as f:
    for line in f:
        for f_key in d.keys():
            if f_key in line:
                pattern = re.compile(r'\s({})(\s|\n)'.format(f_key))
                line = re.sub(pattern,' ' +d[f_key]+' ',line)
                line = re.sub(pattern,' ' +d[f_key]+' ',line)
        if line[-1]!='\n':
            line=line+'\n'
        fout.write(line)        
fout.close()
