#!/usr/bin/env python
# coding=utf-8

import sys 
import re
import urllib2
from tabulate import tabulate

def craw():
    #url = "http://caipiao.163.com/award/cqssc/20170914.html"
    url = "http://chart.cp.360.cn/kaijiang/ssccq/?r_a=QZ7fuy#"
    response = urllib2.urlopen(url)
    print response.code
    html = response.read()
    #print html

    #info = '''<td class="start" data-win-number='(.*)' data-period="(.*)">''' 
    info = """<tr><td class='gray'>(.*)</td><td class='red big'>(.*)</td>"""
    result = re.findall(info, html)
    print result

"""
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


    print tabulate(table)
    #s = tabulate(table)

    i = 0
    s = []
    s.append(table[0][1])
    for i in range(1, len(table)):
        for j in range(0, len(s)):
        if s[j] < int(table[i][1]):
            continue
        else:
            s.append(s[-1])
            for k in range(len(s),j, -1):
                s[k] = s[k-1]
"""

craw()
