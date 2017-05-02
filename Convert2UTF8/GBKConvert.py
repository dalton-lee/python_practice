#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys
import os
import chardet
import codecs

def replaceEncode(filename):

    fileencode = chardet.detect(codecs.open(filename, 'rb').read())['encoding']
    filereader = codecs.open(filename, 'r', fileencode)

    data = filereader.read()
    if data[:3] == codecs.BOM_UTF8:
        data = data[3:]
    filereader.close()

    print(filename)

    filewriter = codecs.open(filename, 'w+', 'utf-8')
    filewriter.write(data)
    filewriter.close()

def recursive(dir):
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            recursive(path)
        else:
            replaceEncode(path)


if __name__=="__main__":

    path = sys.argv[1]
    recursive(path)