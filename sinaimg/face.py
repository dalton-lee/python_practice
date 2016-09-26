#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
from urllib.request import urlopen
import shutil
import os,sys


def download( path, key, datamap):
    for i in range(0, len(datamap)):
        phrase = datamap[i].get('phrase')
        value = datamap[i].get('value')
        if phrase != value:
            print(phrase + ':< phrase - - - - - - - - - - - value >:' + value)
        file = os.path.join(os.path.dirname(path), key, str(i).rjust(3, '0') + '_' + phrase[1:-1] + '.gif')
        url =datamap[i].get('url')
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with urlopen(url) as response, open(file, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

if __name__ == "__main__":

#    http://weibo.com/aj/mblog/face?type=face
    filepath = input(u'请输入你的json文件完整路径:')
    category = input(u'请输入你要下载的图片类别(all下载所有):')
    if not category:
        print(u'请输入正确的图片类别！')
        sys.exit(0)

    with open(filepath, 'r') as f:
        jsonobj = json.load(f, object_pairs_hook=OrderedDict)
    data = jsonobj.get('data')

    usual = data.get('usual')
    more = data.get('more')
    brand = data.get('brand')

    datadict = {}
    for (k, v) in usual.items():
        datadict[k] = v

    for (k, v) in more.items():
        datadict[k] = v

    brandnorm = brand.get('norm')
    for (k, v) in brandnorm.items():
        datadict['norm' + k] = v

    for (k, v) in datadict.items():
        if category == 'all':
            download(filepath, k, v)
        elif category == k:
            download(filepath, k, v)

    print(' - - - - - - - - - happy end - - - - - - - - -')












