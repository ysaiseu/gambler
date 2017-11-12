#!/usr/bin/env python
# coding=utf-8
import sys 
import re
import urllib2
from tabulate import tabulate
import gambler_data

def onQQMessage(bot, contact, member, content):
    if content == '状态':
        bot.SendTo(contact, '还活着')
    elif content == '关闭':
        bot.SendTo(contact, '已关闭')
        bot.Stop()
    elif re.match('查询.*(，.*)*','content'):
        gambler_data.command = content.replace('查询','',1).split('，')
        gambler_data.handle(1)
        gambler_data.command = [command(0),command(1)]
        text = ''
        for i in s:
          text = text + i +'\n'
        bot.sendto(contact,text)