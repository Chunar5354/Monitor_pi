# coding=utf-8

from tornado.tcpserver import TCPServer
from tornado.netutil import bind_sockets
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.ioloop import IOLoop
import json
from fetch_data import Hunter
from rhandler import RedisHandler
import logging
import time
from simu_data import data_magic

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/fetch_data_server/socket.log', level=logging.DEBUG)

class DataServer(TCPServer):

	clients = dict()

	@gen.coroutine
	def handle_stream(self, stream, address):
		"""
		:param stream:
		:param address:
		:return:
		"""
		t = time.localtime()
		logging.info("Socket served at time: {} with: {}".format(time.asctime(t), address))
		DataServer.clients[address] = stream
		while True:
			try:
				logging.info("successfully connected ...")

				data = yield stream.read_bytes(1024, partial=True)
				try:
					data_dict = json.loads(data.decode())
					# get result
					ht = Hunter()
					rh = RedisHandler()
					# If can't find data in redis, fetch it from mysql
					result_dict = {}
					result_dict = rh.outhash(data_dict)
					if not result_dict:
						result_dict = ht.get_data(data_dict) 
					# if need to change voltage data, use the statement below
					# result_dict = data_magic(result_dict)
					data_send = json.dumps(result_dict)
					
					yield stream.write(data_send.encode())
				except KeyError:
					logging.info('** Data Error **')

			except StreamClosedError:
				logging.info("Server finished")
				logging.info("*"*25)
				del DataServer.clients[address]
				break


if __name__ == '__main__':
	server = DataServer()
	sockets = bind_sockets(30105)
	server.add_sockets(sockets)
	IOLoop.current().start()
