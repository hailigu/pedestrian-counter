# -*- coding: utf-8 -*-
# @Time    : 2018/4/5 23:05
# @Author  : DeepKeeper (DeepKeeper@qq.com)
# @Site    :
# @File    : map.py
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import datetime
import logging
import os
import platform
import re
import sys
from subprocess import PIPE

import matplotlib.pyplot as plt
import psutil
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

# just for logger
logging.basicConfig()
logger = logging.getLogger()


def get_file_name_and_ext(filename):
    (file_path, temp_filename) = os.path.split(filename)
    (file_name, file_ext) = os.path.splitext(temp_filename)
    return file_name, file_ext


# log or display some message
def show_message(message, log, stop=False):
    if stop:
        message += "\n\n\n\n"
    if log:
        log.info(message)
    else:
        print(message)
    if stop:
        sys.exit(0)


# parse string to bool
def str2bool(v):
    if not v:
        return False
    return v.lower() in ("yes", "true", "t", "1")


# init logger for apps
def init_logger(log_file, level=logging.INFO):
    logger.setLevel(level)
    fh = logging.FileHandler(log_file)
    logger.addHandler(fh)


parser = argparse.ArgumentParser(description="command")
parser.add_argument('--start', dest='start_num', type=int, default=0,
                    help='start number to process')
parser.add_argument('--end', dest='end_num', type=int, default=0,
                    help='end number to process')
parser.add_argument('--step', dest='step_num', type=int, default=200,
                    help='step number')
parser.add_argument('--type', dest='count_type', type=str, default='map',
                    help='count type')
parser.add_argument('--config_prefix', dest='config_prefix', type=str, default='',
                    help='config file prefix')
parser.add_argument('--data_file', dest='data_file', type=str, default='person.data',
                    help='config file prefix')
parser.add_argument('--weights_prefix', dest='weights_prefix', type=str, default='tiny-yolo-voc-person_9300_9c512_',
                    help='weight file prefix')
parser.add_argument('--base_dir', dest='base_dir', type=str, default='./gender',
                    help='base dir for all files')
parser.add_argument('--weight_dir', dest='weight_dir', type=str, default='backup',
                    help=' dir for weight files')
args = parser.parse_args()

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

end_num = 0
start_num = 0
count_type = ''
if args.start_num > 0:
    start_num = args.start_num
else:
    show_message('start must be not zero', logger, True)

if args.count_type.lower() != 'map' and args.count_type.lower() != 'recall':
    count_type = 'map'
else:
    count_type = args.count_type.lower()

if args.end_num > 0:
    end_num = args.end_num + 200
    LOG_FILE_PATH = os.path.join(APP_ROOT, '{}_{}_{}.log'.format(os.path.join(args.base_dir, args.config_prefix),
                                                                 count_type, args.end_num))
else:
    end_num = start_num + 200
    LOG_FILE_PATH = os.path.join(APP_ROOT, '{}_{}_{}.log'.format(os.path.join(args.base_dir, args.config_prefix),
                                                                 count_type, start_num))

init_logger(LOG_FILE_PATH, logging.INFO)

message = ''
for i in range(start_num, end_num, args.step_num):
    weights = "{}{}.weights".format(os.path.join(args.base_dir, args.weight_dir, args.weights_prefix), str(i))
    print(weights)
    if not os.path.exists(weights):
        show_message('{} not exist'.format(weights), logger)
        continue
    p = psutil.Popen(["./darkneto", "detector", count_type, os.path.join(args.base_dir, args.data_file),
                      "{}.cfg".format(os.path.join(args.base_dir, args.config_prefix)),
                      weights], stdout=PIPE)

    # if platform.system() == 'Windows':
    #     message = p.stdout.read()
    # else:
    #     message = bytes.decode(p.stdout.read())

    message = bytes.decode(p.stdout.read())

    if count_type == 'map':
        message = 'NO.[{}]\r\n'.format(str(i)) + message
    else:
        message = '{}  NO.[{}]\r\n'.format(message, str(i))
    show_message(message, logger)

file_name, _ = get_file_name_and_ext(LOG_FILE_PATH)
content = open(LOG_FILE_PATH).read()

iterations = []
maps = []
fig, ax = plt.subplots()

ymajorLocator = MultipleLocator(1)
# ymajorFormatter = FormatStrFormatter('%1.1f')
yminorLocator = MultipleLocator(0.5)

ax.yaxis.set_major_locator(ymajorLocator)
# ax.yaxis.set_major_formatter(ymajorFormatter)

ax.yaxis.set_minor_locator(yminorLocator)

ax.yaxis.grid(True, which='minor')

if count_type == 'map':
    pattern = re.compile(r"NO.\[(.*?)\][\s\S]*?average IoU = (.*?) %[\s\S]*?\(mAP\).*?, or (.*?) %")
else:
    pattern = re.compile(r"([\d]*): .*?, (.*?) avg,")

matches = pattern.findall(content)
# print(type(matches[0]))
counter = 0
log_count = len(matches)
csv_path = os.path.join(APP_ROOT, '{}_{}.csv'.format(os.path.join(args.base_dir, args.config_prefix),
                                                     count_type))
out_file = open(csv_path, 'w')
out_file.write('iter,map,iou \n')

for match in matches:
    counter += 1
    if log_count > 200:
        if counter % 200 == 0:
            print('parsing {}/{}'.format(counter, log_count))
    else:
        print('parsing {}/{}'.format(counter, log_count))
    iteration, IoU, map_ = match
    iterations.append(int(iteration))
    maps.append(float(map_))
    out_file.write(iteration + ',' + map_ + ',' + IoU + '\n')
print('mAP has been written to {}'.format(os.path.basename(csv_path)))

ax.plot(iterations, maps)
plt.xlabel('Iteration')
plt.ylabel('mAP')
plt.grid()

save_path = os.path.join(APP_ROOT, '{}_{}.png'.format(os.path.join(args.base_dir,
                                                                   args.config_prefix), count_type))
plt.savefig(save_path, dpi=300)
if sys.platform == 'win32':
    plt.show()
