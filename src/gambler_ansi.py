#!/usr/bin/env python
# coding=utf-8

import os
import string
import re
import time
import sys 
import re
import urllib2
from tabulate import tabulate
from qqbot import qqbotsched
from datetime import datetime, timedelta
import threading
import json
import gambler_data

lottery={}
mode_dict = {}
SN = 0
s = []
yujing_flag = 0

@qqbotsched(hour='0-23/1', minute='0-59/1', second='0-59/5')
def mytask(bot):
    global SN
    global s
    s = []
   
    gl = bot.List('group', '测试群')
    man = bot.List('buddy', '开奔驰捡垃圾')
    time0 = time.time()
    info = init()
    print "time = ", time.time() - time0
    SN_new = info[0]
    msg = info[1]
    s_all = '上一期期号 ： ' + str(SN) + '\n'
    s_all = s_all + '当前期号 ： ' + str(SN_new) + '\n'
    s_all = s_all + '当前号码 ： ' + msg + '\n'
    global yujing_flag
    if SN != SN_new:
        SN = SN_new
        #print s
        if yujing_flag == 0:
            return
        else:
            yujing_flag = 0
        if gl is not None:
            for group in gl:
                for s_line in s:
                    s_all = s_all + s_line + '\n'
                bot.SendTo(group, s_all)
                s_all = ''
    '''
    if man is not None:
        for m in man:
            bot.SendTo(m, msg[-1][0])
            bot.SendTo(m, msg[-1][1])
    '''
##  main  ##==================================================================================================================
##  main  ##==================================================================================================================

def init():
    gambler_data.data_handle()

init()