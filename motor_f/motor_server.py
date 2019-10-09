import sys   
import socket
import pymysql
import json
import struct
import threading
from into_db import Motor
import logging
import time

logging.basicConfig(filename='motor.log', level=logging.DEBUG)

class WSGIServer(object):
    def __init__(self, host, port):
        """init"""
        # create a socket object, and declare the type
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # set host and port
        self.server.bind((host, port))

        # start to listen, and there can be 30 connections at most in queue
        self.server.listen(30)
        # instance a Motor object
        self.motor = Motor()
        self.num = 0
        self.jud = True

    def get_data(self, conn, addr):
        """receive data and insert data into database"""
        while self.jud:
            try:
                # length = struct.unpack('i', conn.recv(4))  # rceive the length of data
                data_all = b''
                # l = length[0]
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
                #print('Inserted scuuessfully')
                logging.info('Inserted successfully')

            except:
                #print('data error')
                #print('connection over')
                logging.error('data error')
                logging.warning('connecting over')
                self.num = 0
                conn.close()
                #return
                self.jud = False

    def run(self):
        """get connected"""
        while True:
            conn, addr = self.server.accept()
            #print("connected with: {}".format(addr))
            t = time.localtime()
            logging.info("At time {} connected with: {}".format(time.asctime(t), addr))

            # when a new socket is connected, start a new thread
            t1 = threading.Thread(target=self.get_data, args=(conn, addr), daemon=True)
            t1.start()


def main(host, port):
    fe = open('motor.log', 'a')

    stderr = sys.stderr
    stdout = sys.stdout
    sys.stderr = fe
    sys.stdout = fe

    wsgi_server = WSGIServer(host, port)
    wsgi_server.run()

    fe.close()


if __name__ == '__main__':
    # set host and port
    host, port = '172.26.106.61', 30102
    main(host, port)
