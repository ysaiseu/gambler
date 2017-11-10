#!/usr/bin/env python
# coding=utf-8

import sys 
import re
import urllib2
from tabulate import tabulate
from qqbot import qqbotsched

@qqbotsched(hour='2-13/1', minute='3-59/10')
def mytask(bot):
    gl = bot.List('group', '测试群')
    man = bot.List('buddy', '开奔驰捡垃圾')
    msg = craw()
    print msg
    if gl is not None:
        for group in gl:
            bot.SendTo(group, msg[-1][0])
            bot.SendTo(group, msg[-1][1])
    if man is not None:
        for m in man:
            bot.SendTo(m, msg[-1][0])
            bot.SendTo(m, msg[-1][1])

def craw():
    url = "http://caipiao.163.com/award/cqssc/20170915.html"
    response = urllib2.urlopen(url)
    print response.code
    html = response.read()

    info = '''<td class="start" data-win-number='(.*)' data-period="(.*)">''' 
    result = re.findall(info, html)

    i = 0
    j = 0
    table = [[]]

    while 1:
        for i in range(3):
            if len(result) <= j*3+i:
                print j*3+1
                break
            table[j].append(result[j*3+i])
        if len(result) <= j*3+i:
            break
        table.append([])
        i = 0
        j = j+1


    #print tabulate(table)
    #s = tabulate(table)

    i = 0
    s = []

    for i in range(0, len(result)):
        for j in range(len(result)-1, i, -1):
            if result[j][1] < result[j-1][1]:
                tmp = result[j]
                result[j] = result[j-1]
                result[j-1] = tmp
    
    #print result
        
    return result


