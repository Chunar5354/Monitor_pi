#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socketserver
import socket
import pymysql
import json
import struct
import logging
import time
from fetch_aver import Hunter
from simu_overview import data_magic

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/overview/overview.log', level=logging.DEBUG)

class MyServer(socketserver.BaseRequestHandler):
    """
    必须继承socketserver.BaseRequestHandler类
    """
    def handle(self):
        """
        必须实现这个方法！
        :return:
        """
        ht = Hunter()
        conn = self.request         # request里封装了所有请求的数据
        # conn.sendall('欢迎访问socketserver服务器！'.encode())
        t = time.localtime()
        logging.info("At time {} connected with: {}".format(time.asctime(t), self.client_address))
        while True:
            try:
                data_all = conn.recv(1024)

                # Translate bytes data into dictionary
                data_dict = json.loads(data_all.decode('utf-8'))

                result_dict = ht.get_data(data_dict)
                # simulate voltage data for exhibition, in peacetime, annotate it
                # result_dict = data_magic(result_dict)

                data_send = json.dumps(result_dict)
                conn.sendall(data_send.encode())

            except:
                #logging.error('data error')
                #logging.info('connection over')
                print('data error')
                conn.close()
                return


if __name__ == '__main__':
    # 创建一个多线程TCP服务器
    server = socketserver.ThreadingTCPServer(('172.26.106.61', 30103), MyServer)
    # print("启动socketserver服务器！")
    # 启动服务器，服务器将一直保持运行状态
    server.serve_forever()
