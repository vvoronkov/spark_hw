# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:54:27 2018

@author: Victor
"""
import os

pathlist=["ENG", "test\\1.txt", "test\\1234\\"]
files=[]


for p in pathlist:
    if os.path.exists(p):
        if os.path.isfile(p):
            files.append(p)
        else:
            for root, directories, filenames in os.walk(p):
                for filename in filenames:
                    files.append(os.path.join(root,filename))
#files=traverse_path(pathlist)
for file in files:
    print (file)