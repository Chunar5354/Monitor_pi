import asyncio
import websockets
import pymysql
from sql_helper import Helper
import pandas as pd
import numpy as np
import json

async def hello(websocket, path):
	data = await websocket.recv()
	table_name = '406_' + data

	sql = "select create_time, value from monitoring_test.{} where create_time>'2018-11-27 13:48:23' && create_time<'2018-11-27 13:48:24'".format(table_name)

	result = pd.read_sql(sql, db)  # method from dandas, read mysql into pandas.dataframe
	result = result.astype(str)  # change data type into string 
	num_result = np.array(result)  # change the whole type into list, by using numpy.array
	list_result = num_result.tolist()  # into list
	send_dict = {data: list_result}
	data_send = json.dumps(send_dict)  # translate into str to send

	await websocket.send(data_send)

if __name__ == '__main__':
	db = pymysql.connect(host='',
				user='Chunar',
				password='chun.0927',
				database='monitoring_test',
				port=30106)

	start_server = websockets.serve(hello, "172.26.106.61", 30104)

	asyncio.get_event_loop().run_until_complete(start_server)
	asyncio.get_event_loop().run_forever()
