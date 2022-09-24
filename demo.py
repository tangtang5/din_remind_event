# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 11:50:39 2022

@author: 27166
"""

import xlrd
import time
import datetime
import smtplib
from email.mime.text import MIMEText

import requests
import json
import hmac
import hashlib
import base64
import urllib.parse

# 验证密钥（无需改动，直接照搬，返回url）
def sign():
    # 1、此处填上Webhook链接和密钥
    webhook = "https://oapi.dingtalk.com/robot/send?access_token=ae569514a508b99892f4a2b102eaa75e03bc3a49271c07c1799d63d1251fd9a4"
    secret = "SEC91ef40388152f8805827a898f8901808105d1d84a6b94c5288cf08648a56422b"
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = webhook+'&timestamp='+timestamp+'&sign='+sign
    return url

def get_todayevent(filename):
    XL_COL = 2            #单元表的列数始终为2
    """
        文件读取及日期对照模块
        https://blog.csdn.net/weixin_43405649/article/details/119080975
    """
    xl = xlrd.open_workbook(filename)
    # 获取第一个sheet表格
    table = xl.sheets()[0]
    date_event = []
    row = table.nrows #获取行数，包括名字
    
    col = XL_COL
    for i in range(1,row):
        temp = []
        for j in range(col):
            temp.append(table.cell(i,j).value)
        date_event.append(temp)
    
    today_event = []
    for i in range(len(date_event)):
        date_new = xlrd.xldate_as_datetime(date_event[i][0], 0)
        date_new = str(date_new)
        print(date_new)
        date_new = list(date_new)
        date_new = ''.join(date_new[0:10])
        
        local_time = datetime.datetime.now()
        remind_time = (local_time+datetime.timedelta(days=3)).strftime("%Y-%m-%d")
        remind_time = str(remind_time)
        if remind_time == date_new:
            today_event.append(str(date_event[i][1]))
    return today_event

def remind_email(today_event):
    # """
    #     邮箱提醒模块，也是网上开源的
    #     url:https://zhuanlan.zhihu.com/p/24180606
    # """
    
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.qq.com'
    #163用户名
    #'用户名，一般是@前面的部分'
    mail_user = '271661225'
    #密码(部分邮箱为授权码)
    mail_pass = 'jxueflfxuvfwcafb'
    #邮件发送方邮箱地址
    sender = '271661225@qq.com'
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['271661225@qq.com']
    
    #设置email信息
    #邮件内容设置
    if today_event:
        msg = "your_name,3天前提醒待办事项：" + "、".join(today_event) + "。加油~"
        message = MIMEText(msg,'plain','utf-8')
        #邮件主题
        message['Subject'] = '当前待办事项~'
        #发送方信息
        message['From'] = sender
        #接受方信息
        message['To'] = receivers[0]
    
        #登录并发送邮件
        try:
            smtpObj = smtplib.SMTP()
            #连接到服务器
            smtpObj.connect(mail_host,25)
            #登录到服务器
            smtpObj.login(mail_user,mail_pass)
            #发送
            smtpObj.sendmail(
                sender,receivers,message.as_string())
            #退出
            smtpObj.quit()
            with open("message.log", mode='a') as filename:
                filename.write("邮件成功发送" + "，发送时间" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                filename.write('\n')  # 换行
        except smtplib.SMTPException as e:
            print('发送失败：',e) #打印错误
        
def remind_ding(today_event):
    url = sign()
    header = {
        "Content-Type": "application/json",
        "Charset": "UTF-8"
    }
    if today_event:
        s = []
        init = '陈陈\n你有{}件事需要三天内完成：\n'.format(len(today_event))
        for i in range(len(today_event)):
            p='({})'.format(i+1)+today_event[i]+'\n'
            s.append(p)
        pp = ''.join(s)
        
        # end_p = '加油！'
        
        # msg=init+pp+end_p
        msg=init+pp
        # text样式
        message = {
            "msgtype": "text",
            "text": {
                "content": msg
            },
            "at": {
                "isAtAll": True
                # ,
                # "atUserIds":['陈陈']
            }
        }

        # # markdown样式
        # message = {
        #     "msgtype": "markdown",
        #     "markdown": {
        #         "title":"今日任务提醒",
        #         "text": msg
        #     },
        #     "at": {
        #         "atMobiles": [],
        #         "atUserIds": [],
        #         "isAtAll": False
        #     }
        # }

        # link样式
        # message = {
        #     "msgtype": "link", 
        #     "link": {
        #         "text": "第3条测试信息", 
        #         "title": "近日公告", 
        #         "picUrl": "https://img.zcool.cn/community/01a2485545680f0000019ae9da087c.jpg@1280w_1l_2o_100sh.jpg", 
        #         "messageUrl": "https://developers.dingtalk.com/document/app/custom-robot-access"
        #     }
        # }
        #发送邮件
        try:
            #发送信息
            message_json = json.dumps(message)
            send_message = requests.post(url=url,data=message_json,headers=header)
            print(send_message.text)
        except smtplib.SMTPException as e:
            print('发送失败：',e) #打印错误
    
if __name__=="__main__":
    filename = 'test.xls'
    today_event = get_todayevent(filename)
    print(today_event)
    print(len(today_event))
    remind_ding(today_event) 
    
    