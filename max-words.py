# -*- coding: utf-8 -*-
"""
Created on June 10 20:54:27 2018

@author: Victor
"""
import os
import argparse
import re
import cProfile

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
        #TODO fork here!
        process_file(sPath)
        #TODO merge results!
        
#TODO: support RUS (UTF8)
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
            
    #TODO: acquire lock for global dictionary
    for key in dic_local.keys():
        dic_global[key]=dic_global.get(key, 0)+dic_local[key]
            
        
def main():
    parser = argparse.ArgumentParser(
            description='Display N most frequent words in provided files')
    parser.add_argument('count', type=int, metavar='N', help='number of most frequent words')
    parser.add_argument('files', type=str, nargs='+', help='list of files/dirs to scan')

    #TODO: restore args = parser.parse_args()
    args = parser.parse_args(["5", "ENG\\", "test\\1s.txt"])
    
    validPathExists=0
    for sPath in args.files:
        #TODO: have to assure at least one valid path
        if os.path.exists(sPath):
            traverse_files(sPath)
            validPathExists=1
    
    if validPathExists:
        for word in sorted(dic_global, key=dic_global.get, reverse=True)[:args.count]:
            #TODO: print ("word '%s' occured '%d' times" % (word, dic[word]))    
            print (word, dic_global[word])
    else:
        print("no single valid path exists, please provide at least one")
        parser.print_help()

#cProfile.run('main()')
if __name__ == '__main__':
    main()