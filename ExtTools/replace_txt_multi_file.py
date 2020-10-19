#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/10/13 10:09
# @Author   :   ZANWEB
# @File     :   replace_txt_multi_file.py in anything_test
# @IDE      :   PyCharm


import re
import os


def reset(path):
    i = 0
    filelist = os.listdir(path)  # 该文件夹下所有文件（包括文件夹）
    for files in filelist:  # 遍历所有文件
        i = i + 1
        Olddir = os.path.join(path, files)  # 原来的文件路径
        if os.path.isdir(Olddir):
            continue

        filename = os.path.splitext(files)[0]
        filetype = os.path.splitext(files)[1]
        filePath = path + filename + filetype
        filePath = os.path.join(path, filename+filetype)

        # alter(filePath, "13.50", "14.00")
        alter_any(filePath)


def alter(file, old_str, new_str):
    with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:

            if old_str in line:
                line = line.replace(old_str, new_str)

            f2.write(line)

    os.remove(file)
    os.rename("%s.bak" % file, file)


def alter_any(file):
    # with open(file, "r", encoding="utf-8") as f1, open("%s.bak" % file, "w", encoding="utf-8") as f2:
    with open(file, "r", encoding="gbk") as f1, open("%s.bak" % file, "w", encoding="gbk") as f2:
        for line in f1:
            if ',' in line:
                index = line.find(',')
                line = line[:index]+'\n'
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)


if __name__ == '__main__':
    path_files = r'C:\Users\zzimo\Desktop\double-length-in-nc\2203207\NCFiles'

    reset(path_files)
    print('ok')
