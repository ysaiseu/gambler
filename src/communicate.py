#!/usr/bin/env python
# coding=utf-8
import sys 
import re
import urllib2
from tabulate import tabulate
import gambler_data
import global_data

def onQQMessage(bot, contact, member, content):
    if content == '状态':
        bot.SendTo(contact, '还活着')
    elif content == '关闭':
        bot.SendTo(contact, '已关闭')
        bot.Stop()
    elif re.match('查询.*(，.*)*',content):
        global_data.command = content.replace('查询','',1).split('，')
        gambler_data.data_handle(1)
        global_data.command = []
        text = ''
        for i in global_data.s:
          text = text + i +'\n'
        bot.SendTo(contact,text)
