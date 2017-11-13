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
import global_data

@qqbotsched(hour='0-23/1', minute='0-59/1', second='0-59/10')
def mytask(bot):
    SN = global_data
   
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
    yujing_flag = gambler_data.yujing_flag
    print SN, SN_new
    if SN != SN_new:
        SN = SN_new
        #print s
        if yujing_flag == 0:
            return
        else:
            yujing_flag = 0
        if gl is not None:
            for group in gl:
                s = gambler_data.s
                for s_line in s:
                    s_all = s_all + s_line + '\n'
		gambler_data.s = []
		bot.SendTo(group, s_all)
                s_all = ''
    '''
    if man is not None:
        for m in man:
            bot.SendTo(m, msg[-1][0])
            bot.SendTo(m, msg[-1][1])
    '''

def init():
    result = gambler_data.data_handle(0)
    return result
    
init()
