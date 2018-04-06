# -*- coding: utf-8 -*-
# @Time    : 2018/4/6 22:05
# @Author  : DeepKeeper (DeepKeeper@qq.com)
# @Site    :
# @File    : stat.py

import argparse
import glob
import logging
import math
import os
import random
import sys
import time
from collections import namedtuple


def get_file_name_and_ext(filename):
    (file_path, temp_filename) = os.path.split(filename)
    (file_name, file_ext) = os.path.splitext(temp_filename)
    return file_name, file_ext


def get_files(dir, file_type='*.*', recursive=True):
    all_files = []
    if dir:
        dir = dir.strip()
    if not os.path.isabs(dir):
        dir = os.path.abspath(dir)
    des_dir = os.path.join(dir, file_type)
    for file in glob.glob(des_dir):
        all_files.append(file)
    if recursive:
        sub_dirs = get_dirs(dir)
        for sub_dir in sub_dirs:
            sub_dir = os.path.join(sub_dir, file_type)
            for file in glob.glob(sub_dir):
                all_files.append(file)
    return sorted(all_files)


def get_dirs(dir):
    dirs = []
    for root_dir, sub_dirs, files in os.walk(dir):
        for sub_dir in sub_dirs:
            dirs.append(os.path.join(root_dir, sub_dir))
    return dirs


def show_message(message,log, stop=False):
    if stop:
        message += "\n\n\n\n"
    if log:
        log.info(message)
    else:
        print (message)
    if stop:
        sys.exit(0)
classes = ["male,child","male,young","male,adult","male,senior","male,n/a",
"female,child","female,young","female,adult","female,senior","female,n/a",
"n/a,child","n/a,young","n/a,adult","n/a,senior","n/a,n/a"]
# the directory of ground truth for darknet
in_dir = './labels-c15'

files = get_files(in_dir, '*.txt')
print('{} files to be processed.'.format(len(files)))
count = 0
bbox_count = 0
male_count = 0
female_count = 0
na_count = 0
child_count = 0
young_count = 0
adult_count = 0
senior_count = 0
age_na_count = 0
gender_na_count = 0

for f in files:
    file_name, file_ext = get_file_name_and_ext(f)

    lines = open(f).readlines()
    for line in lines:
        bbox_count += 1
        labels = line.strip().split(" ")
        class_id = int(labels[0])
        if class_id <= 4:
            male_count += 1

            if class_id == 0:
                child_count += 1
            elif class_id == 1:
                young_count += 1
            elif class_id == 2:
                adult_count += 1
            elif class_id == 3:
                senior_count += 1
            else:
                age_na_count += 1
                na_count += 1

        elif 5 <= class_id <= 9:
            female_count += 1

            if class_id == 5:
                child_count += 1
            elif class_id == 6:
                young_count += 1
            elif class_id == 7:
                adult_count += 1
            elif class_id == 8:
                senior_count += 1
            else:
                age_na_count += 1
                na_count += 1
        else:
            na_count += 1

            if class_id == 10:
                gender_na_count += 1
                child_count += 1
            elif class_id == 11:
                gender_na_count += 1
                young_count += 1
            elif class_id == 12:
                gender_na_count += 1
                adult_count += 1
            elif class_id == 13:
                gender_na_count += 1
                senior_count += 1
            else:
                gender_na_count += 1
                age_na_count += 1

    count += 1
    print('{}/{} finished.'.format(count, len(files)))
print('\n\n\n\nbbox no. {}'.format(bbox_count))
print('gender:    male {}  female {}  n/a  {} '.format(male_count, female_count, gender_na_count))
print('age:    child {}  young {}   adult {} senior {}   n/a  {} '.format(child_count, young_count, adult_count,
                                                                          senior_count, age_na_count))
print('ALL n/a  {}'.format(na_count))

