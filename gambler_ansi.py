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

lottery={}
mode_dict = {}
SN = 0
s = []
yujing_flag = 0

@qqbotsched(hour='0-23/1', minute='0-59/1', second='0-59/10')
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

def cold(ran,issue):
  key_list = lottery.keys()
  key_list.sort()
  key_list_re = sorted(key_list,reverse=True)
  index = key_list_re.index(issue)
  count = []
  cold_list = [0,1,2,3,4,5,6,7,8,9]
  for i in range(10):
    count.append(0)
  if ran<(len(key_list_re)-index):
    for i in range(int(ran)):
      for j in lottery[key_list_re[i+index]]:
        count[int(j)] = count[int(j)] + 1
  else:
    for i in range(len(key_list_re)-index):
      for j in lottery[key_list_re[i+index]]:
        count[int(j)] = count[int(j)] + 1
  for i in range(9):
    for j in range(9-i):
      if count[i] > count[i+j+1]:
        t = count[i]
        count[i] = count[i+j+1]
        count[i+j+1] = t
        t = cold_list[i]
        cold_list[i] = cold_list[i+j+1]
        cold_list[i+j+1] = t
  print count
  print cold_list
  print lottery[issue]
  return cold_list

def count_5x(list):
  #global dict_5x
  dict_5x = []
  count_list = [0,0,0,0]
  for i in range(10):
    #dict_5x[i] = 0
    dict_5x.append(0)
  for j in list:
    for i in range(10):
      if i == int(j):
        dict_5x[i] = dict_5x[i] + 1
  for i in range(10):
    if dict_5x[i] > 0:
	  count_list[int(dict_5x[i])-1] = count_list[dict_5x[i]-1] + 1
  if count_list[0] == 5:
    return 120
  elif count_list[0] == 3:
    return 60
  elif count_list[1]  == 2:
    return 30
  elif count_list[2] == 1 and count_list[0] == 2:
    return 20
  elif count_list[2] == 1 and count_list[1] == 1:
    return 10
  elif count_list[3] == 1:
    return 500

def win_5x(a,b):
  if a==b: return 1
  else: return 0
  
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
        '''
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
        '''
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

def win_zusj(num):
  if num[0] == num[1] or num[1] == num[2] or num[0] == num[2]:
    return 1
  else:
    return 0

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
    print "New Message coming!"     #flag to see if the robot is down
    global lottery
    global mode_dict
    result = ['', '']
    #抓取数据，存入文件
    ROOT = '/home/ubuntu/.qqbot-tmp/plugins/'
    now = datetime.now() + timedelta(hours=8)
    yesterday = now - timedelta(days=1)
    date = now.strftime("%Y%m%d")
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
    win_5x_120 = win_list(120)
    win_5x_60 = win_list(60)
    win_5x_30 = win_list(30)
    win_5x_20 = win_list(20)
    win_5x_10 = win_list(10)
    win_5x_500 = win_list(500)
    
    win_back_zusan = win_list(0)
    win_mid_zusan = win_list(8)
    win_first_zusan = win_list(9)
    
    win_back_cold1 = win_list(31)
    win_back_cold2 = win_list(32)
    win_back_cold3 = win_list(33)
    win_back_hot1 = win_list(34)
    win_back_hot2 = win_list(35)
    win_back_hot3 = win_list(36)
    
    win_mid_cold1 = win_list(41)
    win_mid_cold2 = win_list(42)
    win_mid_cold3 = win_list(43)
    win_mid_hot1 = win_list(44)
    win_mid_hot2 = win_list(45)
    win_mid_hot3 = win_list(46)
    
    win_first_cold1 = win_list(51)
    win_first_cold2 = win_list(52)
    win_first_cold3 = win_list(53)
    win_first_hot1 = win_list(54)
    win_first_hot2 = win_list(55)
    win_first_hot3 = win_list(56)

    cold_list = [0,1,2,3,4,5,6,7,8,9]

    one = two = three = four = five = -1
    for i in key_list:
        lottery_num = lottery[i]
        ##后三组六模式
        back = lottery_num[2:5]
        mid = lottery_num[1:4]
        first = lottery_num[0:3]
        win_back_zusan.append(i,win_zusj(back))
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
        win_mid_zusan.append(i,win_zusj(mid))	  
        win_mid_one.append(i,win(mid,two))  ##中三单号千位
        win_mid_two.append(i,win(mid,three))  ##中三单号百位
        win_mid_thr.append(i,win(mid,four))  ##中三单号十位
        a = two                                
        b = choose_b(a,three,four,one,five)    
        win_mid_double1.append(i,win(mid,a,b))   ##中三双号千位百位 
        a = two                                
        b = choose_b(a,four,three,one,five)    
        win_mid_double2.append(i,win(mid,a,b))   ##中三双号千位十位 
        a = three                              
        b = choose_b(a,four,two,one,five)      
        win_mid_double3.append(i,win(mid,a,b))   ##中三双号百位十位 
        a = two                                
        b = choose_b(a,three,four,one,five)    
        c = choose_c(a,b,four,one,five)        
        win_mid_triple.append(i,win(mid,a,b,c))  ##中三杀三个号
        ##前三组六模式                           
        win_first_zusan.append(i,win_zusj(first))	  
        win_first_one.append(i,win(first,one))  ##前三单号万位
        win_first_two.append(i,win(first,two))  ##前三单号千位
        win_first_thr.append(i,win(first,three))  ##前三单号百位
        a = one                                                            
        b = choose_b(a,two,three,four,five)                                
        win_first_double1.append(i,win(first,a,b))  ##前三双号万位千位 
        a = one                                                            
        b = choose_b(a,three,two,four,five)                                
        win_first_double2.append(i,win(first,a,b))  ##前三双号个位十位 
        a = two                                                            
        b = choose_b(a,three,one,four,five)                                
        win_first_double3.append(i,win(first,a,b))  ##前三双号十位百位 
        a = one                                                            
        b = choose_b(a,two,three,four,five)                                
        c = choose_c(a,b,three,four,five)                                  
        win_first_triple.append(i,win(first,a,b,c))   ##前三杀三个号
	    ##五星组选
        judge = count_5x(lottery_num)
        win_5x_120.append(i,win_5x(win_5x_120.mode,judge))
        win_5x_60.append(i,win_5x(win_5x_60.mode,judge))
        win_5x_30.append(i,win_5x(win_5x_30.mode,judge))
        win_5x_20.append(i,win_5x(win_5x_20.mode,judge))
        win_5x_10.append(i,win_5x(win_5x_10.mode,judge))
        win_5x_500.append(i,win_5x(win_5x_500.mode,judge))
        ##冷号热号
        a = str(cold_list[0]); b = str(cold_list[1]); c = str(cold_list[2])
        win_back_cold1.append(i,win(back,a))
        win_back_cold2.append(i,win(back,a,b))
        win_back_cold3.append(i,win(back,a,b,c))
        win_mid_cold1.append(i,win(mid,a))
        win_mid_cold2.append(i,win(mid,a,b))
        win_mid_cold3.append(i,win(mid,a,b,c))
        win_first_cold1.append(i,win(first,a))
        win_first_cold2.append(i,win(first,a,b))
        win_first_cold3.append(i,win(first,a,b,c))
	    
        a = str(cold_list[9]); b = str(cold_list[8]); c = str(cold_list[7])
        win_back_hot1.append(i,win(back,a))
        win_back_hot2.append(i,win(back,a,b))
        win_back_hot3.append(i,win(back,a,b,c))
        win_mid_hot1.append(i,win(mid,a))
        win_mid_hot2.append(i,win(mid,a,b))
        win_mid_hot3.append(i,win(mid,a,b,c))
        win_first_hot1.append(i,win(first,a))
        win_first_hot2.append(i,win(first,a,b))
        win_first_hot3.append(i,win(first,a,b,c))
        ##更新号码
        cold_list = cold(24,i)
        one = lottery_num[0]
        two = lottery_num[1]
        three = lottery_num[2]
        four = lottery_num[3]
        five = lottery_num[4]
        print one,two,three,four,five
   
    ##监控部分
    monitor_list = []
    monitor_list.append(win_back_one.monitor(8,0.0,12))
    monitor_list.append(win_back_two.monitor(8,0.0,12))
    monitor_list.append(win_back_thr.monitor(8,0.0,12))
    monitor_list.append(win_back_double1.monitor(12,0.0,20))
    monitor_list.append(win_back_double2.monitor(12,0.0,20))
    monitor_list.append(win_back_double3.monitor(12,0.0,20))
    monitor_list.append(win_back_triple.monitor(20,0.0,30))

    monitor_list.append(win_mid_one.monitor(8,0.0,12))
    monitor_list.append(win_mid_two.monitor(8,0.0,12))
    monitor_list.append(win_mid_thr.monitor(8,0.0,12))
    monitor_list.append(win_mid_double1.monitor(12,0.0,20))
    monitor_list.append(win_mid_double2.monitor(12,0.0,20))
    monitor_list.append(win_mid_double3.monitor(12,0.0,20))
    monitor_list.append(win_mid_triple.monitor(20,0.0,30))

    monitor_list.append(win_first_one.monitor(8,0.0,12))
    monitor_list.append(win_first_two.monitor(8,0.0,12))
    monitor_list.append(win_first_thr.monitor(8,0.0,12))
    monitor_list.append(win_first_double1.monitor(12,0.0,20))
    monitor_list.append(win_first_double2.monitor(12,0.0,20))
    monitor_list.append(win_first_double3.monitor(12,0.0,20))
    monitor_list.append(win_first_triple.monitor(20,0.0,30))

    monitor_list.append(win_5x_120.monitor(12,0.0,20))
    monitor_list.append(win_5x_60.monitor(8,0.0,12))
    monitor_list.append(win_5x_30.monitor(40,0.0,20))
    monitor_list.append(win_5x_20.monitor(50,0.0,20))
    
    monitor_list.append(win_back_zusan.monitor(12,0.0,20))
    monitor_list.append(win_mid_zusan.monitor(12,0.0,20))
    monitor_list.append(win_first_zusan.monitor(12,0.0,20))
    
    monitor_list.append(win_back_cold1.monitor(5,0.0,12))
    monitor_list.append(win_mid_cold1.monitor(5,0.0,12))
    monitor_list.append(win_first_cold1.monitor(5,0.0,12))
    monitor_list.append(win_back_cold2.monitor(8,0.0,20))
    monitor_list.append(win_mid_cold2.monitor(8,0.0,20))
    monitor_list.append(win_first_cold2.monitor(8,0.0,20))
    monitor_list.append(win_back_cold3.monitor(15,0.0,20))
    monitor_list.append(win_mid_cold3.monitor(15,0.0,20))
    monitor_list.append(win_first_cold3.monitor(15,0.0,20))	
    global yujing_flag
    if if_yujing(monitor_list):
        yujing_flag = 1
        print "预警成功"
    else:
        yujing_flag = 0
        print "当前无预警"

    return result
    

time0 = time.time()
init()
print "time = ", time.time()-time0
