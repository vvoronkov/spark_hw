# -*- coding: utf-8 -*-
"""
Created on June 10 20:54:27 2018

@author: Victor
"""
import os
import argparse
import re
import threading
import cProfile

#TODO: how to determine optimal number of workers?
workers_num=2
workers_data=[{} for _ in range(workers_num)]

whitechars = '\?|\.|\!|\/|\\|\;|\:|`|_|,'
stopwords={"did", "out", "got", "her", "were", "the", "and", "was", "that", "his", "you", "with", "they", "for", "had", "this", "but", "there", "then", "him", "not", "are", "them", "into", "she"}


def process_files(worker_id, filelist):
    """
        read content of file into string and clean white chars, 
        then split, count words locally and update global counters 
    """
    dic_local={}
    for file in filelist:
        document = open(file, 'r')
        text_string = document.read().lower()
        text_string=re.sub(whitechars, '', text_string)
        for word in text_string.split():
            if len(word)>2 and word not in stopwords:
                dic_local[word]=dic_local.get(word, 0)+1
    
    workers_data[worker_id]=dic_local       
    
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

def compute_data(nwords):
    """
        combine data produced by workers and sort
    """
    dic_combined=workers_data[0]
    
    for i in range(1,workers_num):
        for key in workers_data[i].keys():
            dic_combined[key]=dic_combined.get(key, 0)+workers_data[i][key]
    
    for word in sorted(dic_combined, key=dic_combined.get, reverse=True)[:nwords]:
        #TODO: print ("word '%s' occured '%d' times" % (word, dic_combined[word]))    
        print (word, dic_combined[word])

        
def main():
    parser = argparse.ArgumentParser(
            description='Display N most frequent words in provided files')
    parser.add_argument('count', type=int, metavar='N', help='number of most frequent words')
    parser.add_argument('files', type=str, nargs='+', help='list of files/dirs to scan')

    #TODO: args = parser.parse_args()
    args = parser.parse_args(["10", "ENG\\", "test\\1s.txt", "abc", "2", ":#@!"])
    
    files=build_fileslist(args.files)
    
    if len(files):
        bucket_size=1+len(files)//workers_num
        threads = []
        for i in range(workers_num):
            t = threading.Thread(target=process_files, args=(i,files[bucket_size*i:bucket_size*(i+1)]))
            threads.append(t)
            t.start()
        
        for t in threads:
           t.join()
        
        compute_data(args.count)
    else:
        print("no single valid path exists, please provide at least one")
        parser.print_help()

#TODO: looks like multithreading doesn't help much since python run it on single CPU core!!!
#TODO: also cProfile shows most of time spent in locks...
# 50    3.776    0.076    3.776    0.076 {method 'acquire' of '_thread.lock' objects}
cProfile.run('main()')
#if __name__ == '__main__':
#    main()