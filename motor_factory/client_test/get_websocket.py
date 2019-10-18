# 使用websocket连接从服务器上获取数据

from websocket import create_connection
import json

#ws = create_connection("ws://101.200.47.95:893/Monitoring/php/api/websocket_data.php")

#ws = create_connection('ws://39.100.5.176:30108/Monitoring/php/api/new_websocket.php')

ws = create_connection("ws://39.100.5.176:30108/Monitoring/php/new_api/websocket_data.php")
print("Sending data...")

data_send = {"customer_name":"",
"serial_number":"406",
"parameter":["current_A","current_B","current_C"],
"limit":"1",
"start":"2019-09-28 14:47:14.840",
"end":"2019-09-28 14:47:14.880"}

data_str = json.dumps(data_send)

ws.send(data_str)
print("Sent")
result =  ws.recv()
print("Received '%s'" % result)
ws.close()
