# Use asyncio and websocket module, cerate a websocket server
# Fetch data by using setch_aver.py

import asyncio
import websockets
import json
from fetch_aver import Hunter
import time
import logging

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/overview/overview.log', level=logging.DEBUG)

async def hello(websocket, path):
	# get parameters
	data = await websocket.recv()

	# output time as log
	t = time.localtime()
	logging.info('Websocket served at time: {}'.format(time.asctime(t)))

	# translate data format into dictionary
	data_dict = json.loads(data)

	# get result
	ht = Hunter()
	result_dict = ht.get_data(data_dict) 
	data_send = json.dumps(result_dict)  # translate into str to send

	await websocket.send(data_send)

if __name__ == '__main__':
	# start server
	start_server = websockets.serve(hello, "172.26.106.61", 30104)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
