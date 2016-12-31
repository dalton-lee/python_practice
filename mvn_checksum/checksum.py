#! /usr/bin/env python
# -*- coding=utf-8 -*-

import os
import hashlib
import shutil


def walk_dir(homedir):
    filelist = []
    if not os.listdir(homedir):
        shutil.rmtree(homedir)
        print('删除空目录：', homedir)
        return

    for item in os.listdir(homedir):
        filepath = os.path.join(homedir, item)
        if os.path.isdir(filepath):
            walk_dir(filepath)

        if filepath.endswith('.lastUpdated') or filepath.endswith('.sha1-in-progress') or filepath.endswith('.jar-in-progress'):
            os.remove(filepath)
            print('删除下载未完成的文件：', filepath)

        if os.path.isfile(filepath):
            filelist.append(filepath)

    if len(filelist) < 2:
        for item in filelist:
            shutil.rmtree(os.path.dirname(item))
            print('删除只剩_remote.repositories的目录：', item)
    else:
        filename = ''
        pomfile = ''
        for item in filelist:
            fileext = os.path.splitext(item)
            if fileext[1].lower() == '.pom':
                filename = fileext[0]
                pomfile = item

        if filename == '':
            return

        pomsha1file = pomfile + '.sha1'

        if not os.path.exists(pomsha1file):
            os.remove(pomfile)
            print('删除没有.pom.sha1的pom文件：', pomfile)
            return

        pomdata = open(pomfile, 'rb').read()
        pomsha1 = hashlib.sha1(pomdata).hexdigest()

        pomsha1content = open(pomsha1file, 'r').read()

        if pomsha1 != pomsha1content[0:40]:
            os.remove(pomfile)
            os.remove(pomsha1file)
            print('删除pom与sha1文件不匹配的文件：', pomfile)
            return

        jarfile = filename + '.jar'
        jarsha1file = jarfile + '.sha1'

        if os.path.exists(jarfile) and not os.path.exists(jarsha1file):
            os.remove(jarfile)
            print('删除没有.jar.sha1的jar文件：', jarfile)
            return

        elif os.path.exists(jarfile) and os.path.exists(jarsha1file):
            jardata = open(jarfile, 'rb').read()
            jarsha1 = hashlib.sha1(jardata).hexdigest()

            jarsha1content = open(jarsha1file, 'r').read()

            if jarsha1 != jarsha1content[0:40]:
                os.remove(jarfile)
                os.remove(jarsha1file)
                print('删除jar与sha1文件不匹配的文件：', jarfile)
                return

if __name__ == "__main__":

    homedir = 'D:/repo/mvn/repository'

    walk_dir(homedir)