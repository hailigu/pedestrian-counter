# -*- coding: utf-8 -*-
# @Time    : 2018/03/28 22:23
# @Author  : DeepKeeper (DeepKeeper@qq.com)
# @Site    :
# @File    : video_check.py
import requests
import os
import argparse
from moviepy.editor import *

parser = argparse.ArgumentParser(description="command")
parser.add_argument('--prefix', dest='txt_prefix', type=str, default='01',
                        help='text prefix')
args = parser.parse_args()

video_list_file = 'videos{}.txt'.format(args.txt_prefix)
# video_url = 'http://7xop7d.com1.z0.glb.clouddn.com/pi/A27/2018-03-05/09_00_04.mp4'

if not os.path.exists('./videos/'):
    os.mkdir('./videos/')

video_list = open(video_list_file).readlines()
video_count = len(video_list)
count = 0
for i in range(video_count):
    print('processing {}/{}'.format((count+1), video_count))

    all_parts = video_list[i].strip().split('/')
    new_file_name = all_parts[4].lower() + '_' + all_parts[5].replace('-', '_') + '_' + all_parts[6]

    success = True
    try:
        clip = VideoFileClip(video_list[i].strip()).subclip(16, 18)
        clip.write_videofile('./videos/' + new_file_name, audio=False)
        clip.save_frame('./videos/' + new_file_name.replace('mp4', 'jpg'), t='0:0:16')
        count += 1
    except Exception:
        success = False

    if not success:
        count += 1
        continue

