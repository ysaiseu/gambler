#!/usr/bin/env python
# coding=utf-8

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

lottery={}
mode_dict = {}
SN = 0
s = []

@qqbotsched(hour='0-23/1', minute='0-59/1')
def mytask(bot):
    global SN
    global s
    s = []
   
    gl = bot.List('group', '测试群')
    man = bot.List('buddy', '开奔驰捡垃圾')
    info = init()
    SN_new = info[0]
    msg = info[1]
    s_all = '上一期期号 ： ' + str(SN) + '\n'
    s_all = s_all + '当前期号 ： ' + str(SN_new) + '\n'
    s_all = s_all + '当前号码 ： ' + msg + '\n'
    if SN != SN_new:
        SN = SN_new
        #print s
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

    for i in range(len(result)):
        s.append([])
        s[i].append(str(result[i][0]).replace(' ',''))
        s[i].append(result[i][1])
        #print str(result[i][0]).replace(' ','')
        
    return s


def tongji(list,n):
  print "重复序列:"
  for i in list:
    print i," ",
  print "\n"
  print n,"次重复统计：",
  lenth=len(list)
  for i in range(lenth-n+1):
    count=0
    for j in range(n):
      count = count+list[i+j]
    print count," ", 
  print "\n"

def if_yujing(list):
  for i in list:
    if i:
	  return 1
  return 0
  
class win_list:
  def __init__(self,mode):
    self.win={}
    self.mode = mode
  def append(self,issue,if_win):
    self.win[issue]=if_win
  def monitor(self,threshold,pro,times):                   ##监控函数封装于字典类中，所有预警打印直接在此函数中进行，需针对该函数打印部分转化为机器人
    global lottery
    global mode_dict
    global s
    key_list = lottery.keys()
    key_list_re = sorted(key_list,reverse=True)  ##倒序期数键值
    key_list.sort()
    fail = 0
    yes = 0.0
    if len(key_list)>times:
      lenth = len(key_list)-times
      t = times
    else:
      lenth = 0
      t = len(key_list)
    for i in key_list[lenth:]:
      if self.win[i] == 1:
        yes = yes+1
    yes = yes/t
    for i in key_list_re:
      if self.win[i] == 0:
        fail = fail + 1
      elif fail >= threshold or yes < pro:   ##大于阈值 产生预警  以下为主要需要处理的部分
        print "---------------------------------------------"
        print mode_dict[self.mode],"已达到预警条件:"
        print "当前次数:",fail
        print "当前",times,"次成功率：",yes
        print "近期走势:"
        s.append( "---------------------------------------------")
        s.append(mode_dict[self.mode]+" 已达到预警条件:")
        s.append("当前次数: "+str(fail))
        s.append("当前"+str(times)+"次成功率"+str(yes)[0:4])
        s.append("近期走势")
        count = 0
        s.append('')
        if len(key_list)>=100:
          lenth = len(key_list)-99
        else:
          lenth = 0
        for j in key_list[lenth:]:
          if self.win[j] == 0:
            count = count + 1
          else:
            print count,
            s[-1] = s[-1] + str(count) +' '
            count = 0
        print "\n--------------------------------------------"
        s.append('')
        if len(key_list) < times:
            s[-1] = s[-1] + str(yes)[0:4] +' '
        else:
          for index in range(len(key_list)-times+1):
            yes = 0.0
            for j in range(times):
                if self.win[key_list[index+j]]==1:
                    yes = yes+1
            s[-1] = s[-1] + str(yes/times)[0:4] + ' '

        s.append("\n--------------------------------------------")
        return fail
      else:
        return 0

  def display_fail(self,times):
    global lottery
    count = 0
    key_list = lottery.keys()
    key_list.sort()
    fail = 0
    for i in key_list[len(key_list)-times:]:
      if self.win[i] == 0:
        fail = fail + 1
      else:
        print fail,
        fail = 0



##判断是否组三或豹子，组三返回0
def win_zusan(num):
  if num[0] == num[1] or num[1] == num[2] or num[0] == num[2]:
    return 0
  else:
    return 1

##多参函数，判断是否num中是否有a列表中的数字，有任一则返返回0
def win(num,*a):
  if win_zusan(num) == 0:
    return 0
  else:
    for single in a:
      if single == num[0] or single == num[1] or single == num[2]:
        return 0
  return 1

##选号函数1
def choose_b(a,b,c,d,e):
  if a != b:
    return b
  elif a != c:
    return c
  elif a != d:
    return d
  elif a != e:
    return e
  else:
    return (int(a)+1)%10

##选号函数2
def choose_c(a,b,c,d,e):
  if a != c and b != c:
    return c
  elif a != d and b != d:
    return d
  elif a != e and b != e:
    return e
  else:
    return (int(b)+1)%10
##  main  ##==================================================================================================================
##  main  ##==================================================================================================================

def init():
    now = datetime.now() + timedelta(hours=8)
    date = now.strftime("%Y%m%d")
    time = now.strftime("%H:%M:%S")
    print time

    #抓取数据，存入文件
    ROOT = '/home/ubuntu/.qqbot-tmp/plugins/'
    result = ['', '']       #result[0] 储存的是最近的期号，result[1]储存的是要发送的内容
    
    result = craw(date)
    f = open(ROOT+date+'.txt', 'w')
    for r in result:
        f.write(r[0]+' ')
        f.write(r[1]+'\n')
    f.close()

    global lottery
    global mode_dict
    lottery_text = open(ROOT+date+'.txt',"r+")
    line = lottery_text.readline()
    print line
    while line:
        line_s = line.split()
        issue = line_s[1]
        lottery_num = line_s[0]
        lottery[issue] = lottery_num
        line = lottery_text.readline()

    #print lottery
    key_list = lottery.keys()
    #print key_list
    key_list.sort()
    #print key_list

    result[0] = key_list[-1]
    result[1] = lottery[key_list[-1]]

    mode_file = open(ROOT+"mode.txt","r+")
    line = mode_file.readline()
    while line:
        line_s = line.split()
        mode_num = line_s[0]
        mode_name = line_s[1]
        mode_dict[int(mode_num)] = mode_name
        line = mode_file.readline()
    mode_file.close()

    win_back_one = win_list(1)
    win_back_two = win_list(2)
    win_back_thr = win_list(3)
    win_back_double1 = win_list(4)
    win_back_double2 = win_list(5)
    win_back_double3 = win_list(6)
    win_back_triple = win_list(7)

    win_mid_one = win_list(11)
    win_mid_two = win_list(12)
    win_mid_thr = win_list(13)
    win_mid_double1 = win_list(14)
    win_mid_double2 = win_list(15)
    win_mid_double3 = win_list(16)
    win_mid_triple = win_list(17)

    win_first_one = win_list(21)
    win_first_two = win_list(22)
    win_first_thr = win_list(23)
    win_first_double1 = win_list(24)
    win_first_double2 = win_list(25)
    win_first_double3 = win_list(26)
    win_first_triple = win_list(27)

    one = two = three = four = five = -1
    for i in key_list:
        lottery_num = lottery[i]
        ##后三组六模式
        back = lottery_num[2:5]
        win_back_one.append(i,win(back,five))  ##后三单号个位
        win_back_two.append(i,win(back,four))  ##后三单号十位
        win_back_thr.append(i,win(back,three))  ##后三单号百位
        a = five
        b = choose_b(a,three,four,two,one)
        win_back_double1.append(i,win(back,a,b))  ##后三双号个位百位
        a = five
        b = choose_b(a,four,three,two,one)
        win_back_double2.append(i,win(back,a,b))  ##后三双号个位十位
        a = four
        b = choose_b(a,three,five,two,one)
        win_back_double3.append(i,win(back,a,b))  ##后三双号十位百位 
        a = five
        b = choose_b(a,four,three,two,one)
        c = choose_c(a,b,three,two,one)
        win_back_triple.append(i,win(back,a,b,c))  ##后三杀三个号
        ##中三组六模式
        back = lottery_num[1:4]
        win_mid_one.append(i,win(back,two))  ##中三单号千位
        win_mid_two.append(i,win(back,three))  ##中三单号百位
        win_mid_thr.append(i,win(back,four))  ##中三单号十位
        a = two
        b = choose_b(a,three,four,one,five)
        win_mid_double1.append(i,win(back,a,b))  ##中三双号千位百位
        a = two
        b = choose_b(a,four,three,one,five)
        win_mid_double2.append(i,win(back,a,b))  ##中三双号千位十位
        a = three
        b = choose_b(a,four,two,one,five)
        win_mid_double3.append(i,win(back,a,b))  ##中三双号百位十位
        a = two
        b = choose_b(a,three,four,one,five)
        c = choose_c(a,b,four,one,five)
        win_mid_triple.append(i,win(back,a,b,c))  ##中三杀三个号
        ##前三组六模式
        back = lottery_num[0:3]
        win_first_one.append(i,win(back,one))  ##前三单号万位
        win_first_two.append(i,win(back,two))  ##前三单号千位
        win_first_thr.append(i,win(back,three))  ##前三单号百位
        a = one
        b = choose_b(a,two,three,four,five)
        win_first_double1.append(i,win(back,a,b))  ##前三双号万位千位
        a = one
        b = choose_b(a,three,two,four,five)
        win_first_double2.append(i,win(back,a,b))  ##前三双号个位十位
        a = two
        b = choose_b(a,three,one,four,five)
        win_first_double3.append(i,win(back,a,b))  ##前三双号十位百位 
        a = one
        b = choose_b(a,two,three,four,five)
        c = choose_c(a,b,three,four,five)
        win_first_triple.append(i,win(back,a,b,c))  ##前三杀三个号
        ##更新号码
        one = lottery_num[0]
        two = lottery_num[1]
        three = lottery_num[2]
        four = lottery_num[3]
        five = lottery_num[4]
        print one,two,three,four,five
   
    ##监控部分
    monitor_list = []
    monitor_list.append(win_back_one.monitor(6,0.3,12))
    monitor_list.append(win_back_two.monitor(6,0.3,12))
    monitor_list.append(win_back_thr.monitor(6,0.3,12))
    monitor_list.append(win_back_double1.monitor(10,0.2,20))
    monitor_list.append(win_back_double2.monitor(10,0.2,20))
    monitor_list.append(win_back_double3.monitor(10,0.2,20))
    monitor_list.append(win_back_triple.monitor(20,0.1,30))

    monitor_list.append(win_mid_one.monitor(6,0.3,12))
    monitor_list.append(win_mid_two.monitor(6,0.3,12))
    monitor_list.append(win_mid_thr.monitor(6,0.3,12))
    monitor_list.append(win_mid_double1.monitor(10,0.2,20))
    monitor_list.append(win_mid_double2.monitor(10,0.2,20))
    monitor_list.append(win_mid_double3.monitor(10,0.2,20))
    monitor_list.append(win_mid_triple.monitor(20,0.1,30))

    monitor_list.append(win_first_one.monitor(6,0.3,12))
    monitor_list.append(win_first_two.monitor(6,0.3,12))
    monitor_list.append(win_first_thr.monitor(6,0.3,12))
    monitor_list.append(win_first_double1.monitor(10,0.2,20))
    monitor_list.append(win_first_double2.monitor(10,0.2,20))
    monitor_list.append(win_first_double3.monitor(10,0.2,20))
    monitor_list.append(win_first_triple.monitor(20,0.1,30))
  
    if if_yujing(monitor_list):
        print "预警成功"
    else:
        print "当前无预警"

    return result
    

init()
