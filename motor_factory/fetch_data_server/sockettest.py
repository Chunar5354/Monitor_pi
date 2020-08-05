import socketserver
import sys   
import socket
import pymysql
import json
import struct
import threading
import logging
import time
from fetch_data import Hunter
from rhandler import RedisHandler


class MyServer(socketserver.BaseRequestHandler):
	"""
	必须继承socketserver.BaseRequestHandler类
	"""
	def handle(self):
		"""
		必须实现这个方法！
		:return:
		"""
		conn = self.request		 # request里封装了所有请求的数据
		# conn.sendall('欢迎访问socketserver服务器！'.encode())
		ht = Hunter()
		rh = RedisHandler()
		while True:
			data = conn.recv(1024)
			data_dict = json.loads(data.decode())

			result_dict = {}
			result_dict = rh.outhash(data_dict)
			if not result_dict:
				result_dict = ht.get_data(data_dict) 
					# if need to change voltage data, use the statement below
		# result_dict = data_magic(result_dict)
			data_send = json.dumps(result_dict).encode()

			print('send')
			print(len(data_send))
			conn.sendall(struct.pack('i', len(data_send)) + data_send)
			# conn.sendall(data_send)



if __name__ == '__main__':
	# 创建一个多线程TCP服务器
	server = socketserver.ThreadingTCPServer(('172.26.106.61', 30206), MyServer)
	# print("启动socketserver服务器！")
	# 启动服务器，服务器将一直保持运行状态
	server.serve_forever()
