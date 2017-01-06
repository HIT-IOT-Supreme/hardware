#!/usr/bin/env python3
# -*- coding:utf-8 -*-
__author__='bahao'
import socket
import time
from multiprocessing import Process,Queue
import asyncio
def init():
    # 缓冲区
    global __udpserver
    __udpserver= socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    __udpserver.bind(('192.168.1.120', 5613))  # 这里的ip和端口在服务器上使用192.168.1.120,以及监听的端口
    print('Bind Udp on ...5613:端口')
    global __addr
    data, __addr = __udpserver.recvfrom(1024)
    # 0：温度,1:湿度，2：气压，3：烟雾，4：门磁，5：红外渐进光，6：周围环境光，7：继电器，8：加速度
    global __buffer
    __buffer= {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: []}
    # 控制继电器开关
    login()
def ct(cmd):
    ct_open=b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x39\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x39\x00\x00\x00\x00\x00\xcb\x01\x00\xd3\x39\x00\x00\x09'
    ct_close=b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x40\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x40\x00\x00\x00\x00\x00\xcb\x01\x00\xd3\x40\x00\x00\x09'
    if(ct==0):
        __udpserver.send(ct_close,__addr)
    if(ct==1):
        __udpserver.send(ct_open,__addr)
    state=__udpserver.recv(1024)[0]
    if(state[22]==39):
        return 1
    if(state[22]==40):
        return 0

def hallwarnning():
    #os.system.execute('warrnig.py')
    print('门磁传感器发来贺电，你的家园正在遭受入侵！')
def handledata(data):
    if(data[22]==0x50):
        hallwarnning()
    elif(data[22]==0x30):#温度
        datalen=data[34]
        tem=data[35:35+datalen]
        print('温度的长度为', data[34])
        print('温度数据为 :',int(tem))
        pushdata(0,tem)
    elif(data[22]==0x31):#湿度
        datalen=data[34]
        shidata=data[35:35+datalen]
        print('湿度的长度为',datalen)
        print('湿度的数据为',shidata)
        pushdata(1,shidata)
    elif (data[22] == 0x37):#气压
        datalen=data[34]
        qiya=data[35:35+datalen]
        print('气压的长度为',datalen)
        print('气压的数据为',qiya)
        pushdata(2, qiya)
    elif (data[22] == 0x34):#烟雾
        datalen=data[34]
        yanwu=data[35:35+datalen]
        print('烟雾的长度为',datalen)
        print('烟雾的数据为',yanwu)
        pushdata(3, yanwu)
    elif(data[22]==0x42):#门磁
        datalen=data[34]
        mengci=data[35:35+datalen]
        print('门磁的长度为',datalen)
        print('门磁的数据为',mengci)
        pushdata(4, mengci)
    elif (data[22] == 0x32):#红外渐进光
        datalen=data[34]
        hongwai=data[35:35+datalen]
        print('红外渐进光的长度为',datalen)
        print('红外渐进光的数据为',hongwai)
        pushdata(5, hongwai)
    elif (data[22] == 0x38):#周围环境光
        datalen=data[34]
        huanjing=data[35:35+datalen]
        print('周围环境光的长度为',datalen)
        print('周围环境光的数据为',huanjing)
        pushdata(6, huanjing)
    elif (data[22] == 0x55):#继电器
        print('继电器')
        pushdata(7, 7)
    elif (data[22] == 0x36):#加速度
        print("加速度")
        pushdata(8, 8)
    #pass#提取时间、传感器类型、传感器数据

#将处理过后的数据压到缓冲区里边
def pushdata(sensorId,data):
    print('BUFFER LENGTH = ',len(__buffer[sensorId]))
    if len(__buffer[sensorId])==10 :
        __buffer[sensorId].pop(0)
        __buffer[sensorId].append(data)
    elif len(__buffer[sensorId])<10:
        __buffer[sensorId].append(data)
#从Id获取缓冲区的数据
def getdDataFromId(SensorId):
    if __buffer[id]!=None:
        result=__buffer[id][0]
    return result

def sendcmd(id):
    #温度
    cmd0 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x30\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x30\x00\x00\x00\x00\x00\xcb\xfb\x03\xd3\x30\x00\x00\x09'
    #湿度
    cmd1 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x31\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x31\x00\x00\x00\x00\x00\xcb\xfb\x03\xd3\x31\x00\x00\x09'
    cmd2 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x37\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x37\x00\x00\x00\x00\x00\xcb\x70\xc4\xd3\x37\x00\x00\x09'
    cmd3 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x34\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x34\x00\x00\x00\x00\x00\xcb\xcb\xd7\xd3\x34\x00\x00\x09'
    cmd4 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x11\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x11\x00\x00\x00\x00\x00\xcb\xff\xff\xd3\x11\x00\x00\x09'
    #红外渐进光
    cmd5 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x32\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x32\x00\x00\x00\x00\x00\xcb\xfb\x03\xd3\x32\x00\x00\x09'
    #周围环境光
    cmd6 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x38\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x38\x00\x00\x00\x00\x00\xcb\xfb\x03\xd3\x38\x00\x00\x09'
    #继电器
    cmd7 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x55\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x55\x00\x00\x00\x00\x00\xcb\xf1\xa4\xd3\x55\x00\x00\x09'
    cmd8 = b'\x00\x24\x54\x73\x00\x01\x00\x02\x00\x01\x00\x36\x00\x00\x00\x00\xab\xcd\x00\x00\x07\x02\x36\x00\x00\x00\x00\x00\xcb\x4a\x77\xd3\x36\x00\x00\x09'


    #cmd3=b'\xab\xcd\x00\x00\x07\x02\x34\x00\x00\x00\x00\x00\xcb\x01\x00\xd3\x34\x00\x00\x09'
    #温度
    if(id==0):
        __udpserver.sendto(cmd0, __addr)    #烟雾
    elif(id==1):
        __udpserver.sendto(cmd1, __addr)
    elif (id == 2):
        __udpserver.sendto(cmd2, __addr)
    elif (id == 3):
        __udpserver.sendto(cmd3, __addr)
    elif (id == 4):
        __udpserver.sendto(cmd4, __addr)
    elif (id == 5):
        __udpserver.sendto(cmd5, __addr)
    elif (id == 6):
        __udpserver.sendto(cmd6, __addr)
    elif (id == 7):
        __udpserver.sendto(cmd7, __addr)
    elif (id == 8):
        __udpserver.sendto(cmd8, __addr)
def consumer():
    r = ''
    while True:
        data = yield r
        if not data:
            return
        # print('data is :' ,data)
        if len(data) > 16:
            handledata(data)
        # r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    print('start listen...')
    while True:
        data, addr = __udpserver.recvfrom(1024)
        sendcmd(0)
        # sendcmd(1)
        # sendcmd(2)
        # sendcmd(3)
        # sendcmd(4)
        # sendcmd(5)
        # sendcmd(6)
        # sendcmd(7)
        # sendcmd(8)
        print('data is : ',data)
        time.sleep(1)
        # sendcmd(2)
        # print('recved data is ...',data)
        r = c.send(data)
        # print('handler return is: %s' % r)
    # c.close()
def login():
    re = b'\x00\x10\x54\x73\x00\x01\x00\x02\x00\x01\x43\x21\x00\x00\x00\x00'
    data, addr = __udpserver.recvfrom(1024)
    __udpserver.sendto(re,addr)

def start():
    c = consumer()
    produce(c)

if __name__=='__main__':
    init()
    start()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(start())
    # loop.close()
    print('start ok')
    # while True:
    #     print("start listen...")
    #     data,addr = udpserver.recvfrom(1024)
    #     sendcmd(3)
    #     sendcmd(2)
    #     time.sleep(1)
    #     if len(data) > 16:
    #         handledata(data)
    #         print('buffer is : ',buffer)
        #print('data from id 3 is ',getdDataFromId(3))
        # print('Received from %s:%s.' % addr)
        # print('Data is : %s' % data)
        # print('Date length is :',len(data))
        # handledata(data)