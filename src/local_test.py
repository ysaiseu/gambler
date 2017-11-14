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

Init_finish = -1
run_flag = 1

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
        global Init_finish
        if Init_finish == -1:
            print "等待初始化。。。。"
        while 1:
            if Init_finish == -1:
                raw_input()
                print "等待初始化。。。。"
                continue
            elif Init_finish == 1:
                print "输入q/Q退出，可以输入其他命令"
                Init_finish = 2
            content = raw_input() 
            if content == 'q' or content == 'Q':
                print "正在退出。。。。"
                global run_flag
                run_flag = 0
                break
            if re.match('查询.*(，.*)*', content):
                global_data.command = content.replace('查询','',1).split('，')
                gambler_data.data_handle(1)
                global_data.command = [0, 20]
                break
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

    while run_flag:
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
        t3.start()
        t1.join()
        result1 = t1.get_result()
        if result1:
            logging.info('get info success')
            Init_finish = 1 if Init_finish == -1 else 0
        else:
            time.sleep(5)
            continue
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

        t2.start()
        t2.join()
        if run_flag == 0:
            break
        result2 = t2.get_result()
        SN_new = result2[0]
        if SN_new != global_data.SN:
            global_data.SN = SN_new
            s_all = '上一期期号 ： ' + str(global_data.SN) + '\n'
            s_all = s_all + '当前期号 ： ' + str(SN_new) + '\n'
            s_all = s_all + '当前号码 ： ' + result2[1] + '\n'
            print s_all
            for info in global_data.s:
                print info
            logging.info(global_data.s)

        t3.join(10)
