# -*- coding: utf-8 -*-
"""
Created on June 10 20:54:27 2018

@author: Victor
"""
import os
import argparse
import re
import time
import multiprocessing
from multiprocessing import Pool


whitechars = '\?|\.|\!|\/|\\|\;|\:|`|_|,'
stopwords={"did", "out", "got", "her", "were", "the", "and", "was", "that", "his", "you", "with", "they", "for", "had", "this", "but", "there", "then", "him", "not", "are", "them", "into", "she"}


def process_files(filelist):
    """
        read content of each file from list into string,
        clean white chars, then split and count words 
    """
    dic_local={}
    for file in filelist:
        document = open(file, 'r')
        text_string = document.read().lower()
        text_string=re.sub(whitechars, '', text_string)
        for word in text_string.split():
            if len(word)>2 and word not in stopwords:
                dic_local[word]=dic_local.get(word, 0)+1
    return dic_local       
    

def build_fileslist(pathlist):
    """
        build flat list of files
    """
    files=[]
    for p in pathlist:
        if os.path.exists(p):
            if os.path.isfile(p):
                files.append(p)
            else:
                for root, directories, filenames in os.walk(p):
                    for filename in filenames:
                        files.append(os.path.join(root,filename))
    return files


def compute_data(workers_data, nwords):
    """
        combine data produced by workers and sort
    """
    dic_combined=workers_data[0]
    
    for i in range(1,len(workers_data)):
        for key in workers_data[i].keys():
            dic_combined[key]=dic_combined.get(key, 0)+workers_data[i][key]
    
    for word in sorted(dic_combined, key=dic_combined.get, reverse=True)[:nwords]:
        print ("word '%s' occured '%d' times" % (word, dic_combined[word]))    


def generate_workers_input(files, workers_num):
    worker_input=[]
    bucket_size=len(files)//workers_num
    if bucket_size*workers_num < len(files):
        bucket_size= bucket_size+1
    for i in range(workers_num):
        worker_input.append(files[bucket_size*i:bucket_size*(i+1)])
    return worker_input

            
def main():
    parser = argparse.ArgumentParser(
            description='Display N most frequent words in provided files')
    parser.add_argument('count', type=int, metavar='N', help='number of most frequent words')
    parser.add_argument('files', type=str, nargs='+', help='list of files/dirs to scan')
    args = parser.parse_args()
    
    files=build_fileslist(args.files)
    
    if len(files):
        startTime = time.time()
        workers_num=multiprocessing.cpu_count()
        worker_input=generate_workers_input(files, workers_num)
            
        pool = Pool(processes=workers_num)
        workers_data=pool.map(process_files, worker_input)
        
        compute_data(workers_data, args.count)
        
        endTime = time.time()
        print ("The job took " + str(endTime - startTime) + " seconds to complete")
    else:
        print("no single valid path exists, please provide at least one")
        parser.print_help()

if __name__ == '__main__':
    main()