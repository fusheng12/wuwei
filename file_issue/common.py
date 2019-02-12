#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time    : 2018/12/26 19:47
# @Author  : WangKang

import os
import time

def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

def file_size(file_path):
    # 获取文件大小 获取到的文件大小为：字节（B）千字节（KB）
    size = os.path.getsize(file_path)
    if size < 1024:
        size = str(size) + "byte"
    elif size >= 1024 and size < 1024 ** 2:
        size = str(round(size / float(1024), 2)) + "K"
    elif size >= 1024 ** 2 and size < 1024 ** 3:
        size = str(round(size / float(1024 ** 2), 2)) + "M"
    else:
        size = str(round(size / float(1024 ** 3), 2)) + "G"
    return size

def file_info(file):
    create_time = TimeStampToTime(os.path.getctime(file))
    size = file_size(file)
    return [create_time, size, 'admin']


if __name__ == "__main__":
    file_info('upload/123.txt')