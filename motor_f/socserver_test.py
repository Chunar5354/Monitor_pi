import socketserver
import sys   
import socket
import pymysql
import json
import struct
import threading
from into_db import Motor
import logging
import time

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_f/motor.log', level=logging.DEBUG)

class MyServer(socketserver.BaseRequestHandler):

    def handle(self):
        self.motor = Motor()
        conn = self.request         # request里封装了所有请求的数据
        t = time.localtime()
        logging.info("At time {} connected with: {}".format(time.asctime(t), self.client_address))
        while True:
            try:
                #length = struct.unpack('i', conn.recv(4))  # rceive the length of data
                data_all = b''
                
                #l = length[0]
                l = 23948  # Sometimes data has a stable length

                # get all of data
                while l > 0: 
                    data = conn.recv(l)
                    data_all += data
                    l -= len(data)

                # Translate bytes data into dictionary
                data_dict = json.loads(data_all.decode('utf-8'))

                # insert data into database
                self.motor.insert_data(data_dict)
                logging.info('Inserted scuuessfully')

            except:
                logging.error('data error')
                logging.warning('connection over')
                conn.close()
                return


if __name__ == '__main__':
    # 创建一个多线程TCP服务器
    server = socketserver.ThreadingTCPServer(('172.26.106.61', 30102), MyServer)
    # 启动服务器，服务器将一直保持运行状态
    server.serve_forever()
