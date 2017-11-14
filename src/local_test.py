#!/usr/bin/env python
# coding=utf-8

import os
import time
import subprocess 
import logging
import threading
import urllib2
import re
import string
from datetime import datetime, timedelta
import socket
import global_data
import gambler_data

exit = 1

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
    try:
        response = urllib2.urlopen(url, timeout = 10)
        html = response.read()
    except urllib2.URLError, e:
        logging.info("raise url error in craw data")
        #print("raise url error in craw data")
        return
    except socket.timeout, e:
        logging.info("raise timeout in craw data")
        #print("raise timeout in craw data")
        return
    #print response.code

    info = '''<td class="start" data-win-number='(.*)' data-period="(.*)">''' 
    result = re.findall(info, html)

    i = 0
    j = 0
    table = [[]]

    while 1:
        for i in range(3):
            if len(result) <= j*3+i:
                #print j*3+1
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

class CrawThread(threading.Thread):
    def __init__(self,date):
        threading.Thread.__init__(self, name = "CrawThread") 
        self.date = date
        self.result = []
    def run(self):
        self.result = craw(self.date)
    def get_result(self):
        return self.result

class ShowThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "ShowThread") 
        self.result = []
    def run(self):
        self.result = gambler_data.data_handle(0)
    def get_result(self):
        return self.result

class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, name = "InputThread") 
        self.result = ''
    def run(self):
        while 1:
            self.result = raw_input() 
            if self.result == 'q' or self.result == 'Q':
                global exit
                exit = 0
                return self.result
            if re.match('查询.*(，.*)*', self.result):
                global_data.command = self.result.replace('查询','',1).split('，')
                gambler_data.data_handle(1)
                global_data.command = []
                text = ''
                for i in global_data.s:
                    text = text + i +'\n'
                return self.result
            print "命令格式有误"

    def get_result(self):
        return self.result

if __name__ == "__main__":
    time_beat = 0
    time_count = 20
    result = []
    result1 = []
    yesterday_init = 0

    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='../log/logger.log',
                        filemode='w+')

    while exit:
        now = datetime.now() + timedelta(hours=8)
        yesterday = now - timedelta(days=1)
        date = now.strftime("%Y%m%d")
        yesterdate = yesterday.strftime("%Y%m%d")
        time0 = now.strftime("%H:%M:%S")
        logging.info(str(time0))

        #抓取数据，存入文件
        #ROOT_DATA = '/home/ubuntu/.qqbot-tmp/plugins/data/'
        ROOT_DATA = '../data/'
    
        t1 = CrawThread(date)  
        t2 = ShowThread()
        t3 = InputThread()
        t1.start()  
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        result1 = t1.get_result()
        result2 = t2.get_result()
        SN_new = result2[0]
        if SN_new != global_data.SN:
            for info in global_data.s:
                print info
            logging.info(global_data.s)

        if result1:
            logging.info('get info success')

        if yesterday_init == 0: 
            time.sleep(10)
            t1 = CrawThread(yesterdate)  
            t1.start()  
            t1.join()
            result1 = t1.get_result()
            if result1:
                logging.info('get yesterday info success')
                yesterday_init = 1

        f = open(ROOT_DATA+date+'.txt', 'w')
        if result is None or result1 is None:
            f.close()
            continue
        for r in result:
            f.write(r[0]+' ')
            f.write(r[1]+'\n')
        for r in result1:
            f.write(r[0]+' ')
            f.write(r[1]+'\n')
        f.close()

        t3.join(10)
        #time.sleep(10)
