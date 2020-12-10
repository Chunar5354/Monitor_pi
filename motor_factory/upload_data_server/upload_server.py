# coding=utf-8

from tornado.tcpserver import TCPServer
from tornado.netutil import bind_sockets
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
import json
import logging
import time
import struct
from into_db import Motor
from rhandler import RedisHandler

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
				read_l = yield stream.read_bytes(4, partial=True)
				length = struct.unpack('i', read_l)
				# print(length)
				logging.info("successfully connected ...")
				data_all = b''
				# l = 23948
				l = length[0]
				while l > 0:
					data = yield stream.read_bytes(l, partial=True)
					data_all += data
					l -= len(data)
				try:
					data_dict = json.loads(data_all.decode())
					motor = Motor()
					rh = RedisHandler()
					# Insert data into redis and mysql
					# rh.inhash(data_dict.copy())
					motor.insert_data(data_dict)
					logging.info('Inserted successfully')
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
