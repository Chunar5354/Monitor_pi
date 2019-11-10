# coding=utf-8

from tornado.tcpserver import TCPServer
from tornado.netutil import bind_sockets
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
import json
import logging
import time
from into_db import Motor

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/upload_data_server/upload.log', level=logging.DEBUG)

class DataServer(TCPServer):
    clients = dict()

    @gen.coroutine
    def handle_stream(self, stream, address):
        """
		Args:
        	stream:
        	address:
        """
        t = time.localtime()
        logging.info("Socket served at time: {} with: {}".format(time.asctime(t), address))
        DataServer.clients[address] = stream
        while True:
            try:
                logging.info("successfully connected ...")
                data_all = b''
                l = 23948
                while l > 0:
                    data = yield stream.read_bytes(1024, partial=True)
                    data_all += data
                    l -= len(data)
                try:
                    data_dict = json.loads(data_all.decode())
                    motor = Motor()
                    motor.insert_data(data_dict)
                    # logging.info('Inserted successfully')
                except KeyError:
                    logging.error('** Data Error **')

            except StreamClosedError:
                logging.info("Server finished")
                logging.info("*"*25)
                del DataServer.clients[address]
                break


if __name__ == '__main__':
    server = DataServer()
    sockets = bind_sockets(30102)
    server.add_sockets(sockets)
    IOLoop.current().start()
