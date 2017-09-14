#!/usr/bin/env python
# coding=utf-8

def onQQMessage(bot, contact, member, content):
    b = bot.List('buddy', '逍遥闲人')
    if content == '你好':
        bot.SendTo(b[0], '我是机器人风')
    elif content == '关闭':
        bot.SendTo(contact, '你无权关闭')
        #bot.Stop()
