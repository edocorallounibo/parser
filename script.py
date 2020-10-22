#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 17:56:43 2020

@author: edoardo
"""
_in=input("input")
_out=input("output")

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
                line = line.replace(f_key,d[f_key])
        fout.write(line)        
fout.close()
