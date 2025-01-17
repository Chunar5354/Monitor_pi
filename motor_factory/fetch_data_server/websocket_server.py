# Websocket server using tornado
import tornado
import tornado.websocket
from fetch_data import Hunter
from rhandler import RedisHandler
import logging
import json
import time
from simu_data import data_magic

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/fetch_data_server/websocket.log', level=logging.DEBUG)

class EchoWebSocket(tornado.websocket.WebSocketHandler):

	# rewrite this methos so that the connection can allow all address
	def check_origin(self, origin):
		return True

	# while start a new connection, log the time
	def open(self):
		t = time.localtime()
		logging.info('Websocket served at time: {}'.format(time.asctime(t)))

	# deal with data fetching
	def on_message(self, message):
		data = message

		# translate data format into dictionary
		data_dict = json.loads(data)

		# get result
		ht = Hunter()
		rh = RedisHandler()
		result_dict = {}
		# If can'f fetch data from redis, fetch data from mysql
		result_dict = rh.outhash(data_dict)
		if not result_dict:
			result_dict = ht.get_data(data_dict) 
		# if need to change voltage data, use the statement below
		# result_dict = data_magic(result_dict)
		data_send = json.dumps(result_dict)  # translate into str to send

		self.write_message(data_send)

	def on_close(self):
		logging.info('*'*10 + 'WebSocket closed' + '*'*10)


if __name__=='__main__':
	app = tornado.web.Application([
		(r'/', EchoWebSocket),
	])
	app.listen(30110)  # set the port, the url will be "ws://ip:30104"
	tornado.ioloop.IOLoop.current().start()
