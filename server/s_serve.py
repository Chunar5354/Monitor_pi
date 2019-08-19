import socket
import pymysql
import json
import struct
import threading
from into_db import Motor


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

    def get_data(self, conn, addr):
        """receive data and insert data into database"""
        while True:
            try:
                length = struct.unpack('i', conn.recv(4))  # rceive the length of data
                data = conn.recv(length[0])

                # Translate bytes data into dictionary
                data_dict = json.loads(data.decode())

                # insert data into database
                self.motor.insert_data(data_dict)

                # check
                print('recive:', data.decode())  # decode the data and print
                conn.send(data.upper())  # send data back
            except:
                print('data error')

    def run(self):
        """get connected"""
        while True:
            conn, addr = self.server.accept()
            print("connected with: {}".format(addr))

            # when a new socket is connected, start a new thread
            t1 = threading.Thread(target=self.get_data, args=(conn, addr))
            t1.start()


def main(host, port):
    wsgi_server = WSGIServer(port)
    wsgi_server.run()


if __name__ == '__main__':
    # set host and port
    host, port = '172.17.52.39', 9876
    main(host, port)
