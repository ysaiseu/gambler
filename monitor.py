#!/usr/bin/env python
# coding=utf-8

import os
import time
import subprocess 
import logging

def count_f():
    f = open("daemon-505455347.log")
    lines = f.readlines()
    count = 0
    count_qc = 0
    count_qc += lines[-1].count('二维码已失效')
    for line in lines:
        count += line.count('New Message')
    f.close()
    result = [count, count_qc]
    return result

def reboot():
    res = subprocess.Popen('ps -ef | grep qq', stdout=subprocess.PIPE,shell=True)
    attn = res.stdout.readlines()
    data = []
    cmd = []
    for at in attn:
        if at.find('qqbot') > -1:
            data.append(at.split()[1])

    #os.system('sudo qq stop')
    for d in data:
        cmd.append('kill '+d)

    for c in cmd:
        os.system(c)

    os.system('qqbot -u ysai')

def craw(date):
    url = "http://caipiao.163.com/award/cqssc/"+date+".html"
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

    i = 0
    s = []

    for i in range(0, len(result)):
        for j in range(len(result)-1, i, -1):
            if result[j][1] < result[j-1][1]:
                tmp = result[j]
                result[j] = result[j-1]
                result[j-1] = tmp
    

    for i in range(len(result)):
        s.append([])
        s[i].append(str(result[i][0]).replace(' ',''))
        s[i].append(result[i][1])
        
    return s

if __name__ == __"main":_
    time_beat = 0
    count_pre = count_f()[0]
    time_count = 10
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='logger.log',
                        filemode='w+')

    while 1:
        time.sleep(20)
        get_count = count_f()
        count = get_count[0]
        count_qc = get_count[1]
        time_beat += 1
        if time_beat >= time_count:
            time_beat = 0
        if time_beat == 0:
            if count == count_pre:
                if count_qc == 0:
                    reboot()
                    logging.info('reboot')
                else:
                    logging.info('need to reget qc')
            else:
                logging.info('nothing happened')
            count_pre = count
