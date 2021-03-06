#!/usr/bin/env python
# coding=utf-8

import time
from datetime import datetime, timedelta
import json
import global_data

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
  lottery = global_data.lottery
  key_list = lottery.keys()
  key_list.sort()
  key_list_re = sorted(key_list,reverse=True)
  index = key_list_re.index(issue)
  count_dict = {0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,9:0}
  cold_list = [0,1,2,3,4,5,6,7,8,9]

  if ran<(len(key_list_re)-index):
    for i in range(int(ran)):
      for j in lottery[key_list_re[i+index]]:
        count_dict[int(j)] = count_dict[int(j)] + 1
  else:
    for i in range(len(key_list_re)-index):
      for j in lottery[key_list_re[i+index]]:
        count_dict[int(j)] = count_dict[int(j)] + 1

  return count_dict

def count_5x(list):
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
    lottery = global_data.lottery
    mode_dict = global_data.mode_dict
    s = global_data.s
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
            s[-1] = s[-1] + str(count) +' '
            count = 0
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
        global_data.s = s
        return fail
      else:
        return 0

def display(self,times):
    lottery = global_data.lottery
    mode_dict = global_data.mode_dict
    s = global_data.s
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
    for j in key_list_re:
      if self.win[j] == 0:
        fail = fail + 1
      else:
        break
    s.append("--------------------------------------------")
    s.append("当前次数: "+str(fail))
    s.append("当前"+str(times)+"次成功率"+str(yes))
    s.append("近期走势：")
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
        s[-1] = s[-1] + str(count) +' '
        count = 0
    s.append('')
    if len(key_list) < times:
      s[-1] = s[-1] + "期数不足总数：" + str(yes)[0:4]
    else:
      for index in range(len(key_list)-times+1):
        yes = 0.0
        for j in range(times):
            if self.win[key_list[index+j]]==1:
                yes = yes+1
        s[-1] = s[-1] + str(yes/times)[0:4] + ' '
    s.append("--------------------------------------------")
    global_data.s = s



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

def query(*command):
    lottery = global_data.lottery
    mode_dict = global_data.mode_dict
    s = global_data.s
    key_list = lottery.keys()
    key_list.sort()
    if command[0] == '冷号':
        cold_list = cold(command[1],key_list[-1])
        s.append(command[1]+'期冷号：')
        s.append('')
        for i in sorted(global_data.cold_dict.items(), key=lambda d:d[1],reverse=False):
            s[-1] = s[-1] + str(i[0]) + ':' + str(i[1]) + '次，'
    else:
        try:
            global_data.set_name_dict()
            name = globals()[global_data.name_dict[int(command[0])]]
            s.append("--------------------------------------------")
            s.append(mode_dict[int(command[0])])
            name.display(int(command[1]))
        except ValueError:
            s.append("命令类型有误")
        except ZeroDivisionError:
            s.append("期数不能为零")  
        else:
            s.append("无对应模式")
    global_data.s = s

def data_handle(run):
    mode_dict = global_data.mode_dict
    result = ['', '']
    if global_data.system_type == 1:
        ROOT = '/home/ubuntu/.qqbot-tmp/plugins/'
    #else:
    #    ROOT = 'd:/users/xinhu/documents/github/gambler/'
    else:
        ROOT = '../'
    ROOT_DATA = ROOT + 'data/'
    ROOT_CONFIG = ROOT + 'config/'
    now = datetime.now() + timedelta(hours=8)
    yesterday = now - timedelta(days=1)
    date = now.strftime("%Y%m%d")
    lottery_text = open(ROOT_DATA+date+'.txt',"r+")
    ##lottery_text = open('number.txt',"r+")
    line = lottery_text.readline()

    with open(ROOT_CONFIG+"config1.json") as config_f:
        config_dict = json.load(config_f)
        dict_item = config_dict[0]
    
    dict_title = dict_item.keys()
    dict_value = dict_item.values()

    while line:
        line_s = line.split()
        issue = line_s[1]
        lottery_num = line_s[0]
        global_data.lottery[issue] = lottery_num
        line = lottery_text.readline()

    lottery = global_data.lottery
    key_list = lottery.keys()
    key_list.sort()

    result[0] = key_list[-1]
    result[1] = lottery[key_list[-1]]

    mode_file = open(ROOT_CONFIG+"mode.txt","r+")
    line = mode_file.readline()
    while line:
        line_s = line.split()
        mode_num = line_s[0]
        mode_name = line_s[1]
        mode_dict[int(mode_num)] = mode_name
        line = mode_file.readline()
    mode_file.close()

    #init for such like win_back_two = win_list(2)
    for key,value in dict_item.items():
        globals()[key] = win_list((int)(value['init']))

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
        global_data.cold_dict = cold(24,i)
        
        cold_list=[]
        for i in sorted(global_data.cold_dict.items(), key=lambda d:d[1],reverse=False):
          cold_list.append(i[0])

        one = lottery_num[0]
        two = lottery_num[1]
        three = lottery_num[2]
        four = lottery_num[3]
        five = lottery_num[4]

    ##监控部分
    if run == 0:
        global_data.s = []
        monitor_list = []
        for key,value in dict_item.items():
                monitor_str = value['monitor'].split(',')
                if monitor_str[0] != '-1':
                    monitor_list.append(globals()[key].monitor((float)(monitor_str[0]),(float)(monitor_str[1]),(int)(monitor_str[2])))
        
        if if_yujing(monitor_list):
            global_data.yujing_flag = 1
        else:
            global_data.yujing_flag = 0
    elif run == 1:
        global_data.s = []
        query(global_data.command[0],global_data.command[1])
        for i in global_data.s:
            print i
        
    return result

if __name__ == '__main__':
    print data_handle(0)

