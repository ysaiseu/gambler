#!/usr/bin/env python
# coding=utf-8
import platform
import json

lottery={}
mode_dict = {}
SN = 0
cold_dict = {}
s = []
yujing_flag = 0
command = [0,20]
system_type = 1 if platform.platform().find('Linux') == 0 else 0
name_dict = {}

'''
name_dict = {1:'win_back_one',2:'win_back_two',3:'win_back_thr',4:'win_back_double1',
  5:'win_back_double2',6:'win_back_double3',7:'win_back_triple',11:'win_mid_one',
  12:'win_mid_two',13:'win_mid_thr',14:'win_mid_double1',15:'win_mid_double2',
  16:'win_mid_double3',17:'win_mid_triple',21:'win_first_one',22:'win_first_two',
  23:'win_first_thr',24:'win_first_double1',25:'win_first_double2',26:'win_first_double3',27:'win_first_triple',
  120:'win_5x_120',60:'win_5x_60',30:'win_5x_30',20:'win_5x_20',10:'win_5x_10',500:'win_5x_500',
  0:'win_back_zusan',8:'win_mid_zusan',9:'win_first_zusan',
  31:'win_back_cold1',32:'win_back_cold2',33:'win_back_cold3',34:'win_back_hot1',35:'win_back_hot2',36:'win_back_hot3',
  41:'win_mid_cold1',42:'win_mid_cold2',43:'win_mid_cold3',44:'win_mid_hot1',45:'win_mid_hot2',46:'win_mid_hot3',
  51:'win_first_cold1',52:'win_first_cold2',53:'win_first_cold3',54:'win_first_hot1',55:'win_first_hot2',56:'win_first_hot3'}
'''

def set_name_dict():
    global name_dict
    with open("../config/config1.json") as f:
        config_dict = json.load(f)
        dict_item = config_dict[0]
    for d in dict_item.items():
        name_dict[(int)(d[1]['init'])] = d[0]
