# -*- coding: utf-8 -*-
"""
Created on June 10 20:54:27 2018

@author: Victor
"""
import os
import argparse
import re
#import cProfile

dic_global={}
stopwords={"did", "out", "got", "her", "were", "the", "and", "was", "that", "his", "you", "with", "they", "for", "had", "this", "but", "there", "then", "him", "not", "are", "them", "into", "she"}

def traverse_files(sPath):
    """
        scan for files recursively in case the path is dir
    """
    if os.path.isdir(sPath):
        for sChild in os.listdir(sPath):
            traverse_files(os.path.join(sPath, sChild))
    else:
        process_file(sPath)
        
def process_file(sPath):
    """
        read content of file into string and clean white chars, 
        then split, count words locally and update global counters 
    """
    dic_local={}
    document = open(sPath, 'r')
    text_string = document.read().lower()
    whitechars = '\?|\.|\!|\/|\\|\;|\:|`|_|,'
    text_string=re.sub(whitechars, '', text_string)
    for word in text_string.split():
        if len(word)>2 and word not in stopwords:
            dic_local[word]=dic_local.get(word, 0)+1
            
    for key in dic_local.keys():
        dic_global[key]=dic_global.get(key, 0)+dic_local[key]
            
        
def main():
    files=[]
    parser = argparse.ArgumentParser(
            description='Display N most frequent words in provided files')
    parser.add_argument('count', type=int, metavar='N', help='number of most frequent words')
    parser.add_argument('files', type=str, nargs='+', help='list of files/dirs to scan')

    #TODO: args = parser.parse_args()
    args = parser.parse_args(["10", "ENG\\", "test\\1.txt", "abc", "2", ":#@!"])
    
    for p in args.files:
        if os.path.exists(p):
            if os.path.isfile(p):
                files.append(p)
            else:
                for root, directories, filenames in os.walk(p):
                    for filename in filenames:
                        files.append(os.path.join(root,filename))
    
    if len(files):
        print (files)
        for f in files:
            process_file(f)
        
        for word in sorted(dic_global, key=dic_global.get, reverse=True)[:args.count]:
            #TODO: print ("word '%s' occured '%d' times" % (word, dic_global[word]))    
            print (word, dic_global[word])
    else:
        print("no single valid path exists, please provide at least one")
        parser.print_help()

#cProfile.run('main()')
if __name__ == '__main__':
    main()