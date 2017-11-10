#!/usr/bin/env python
# coding=utf-8

import sys 
import re
import urllib2
from tabulate import tabulate


def onQQMessage(bot, contact, member, content):
    if content == '状态':
        bot.SendTo(contact, '还活着')
    elif content == '关闭':
        bot.SendTo(contact, '已关闭')
        bot.Stop()
