# 使用socket连接从服务器上获取数据
# 通过修改端口可也可以测试数据总览的socket端

import socket
import json

#host = '101.200.47.95'
#port = 1024

host = '39.100.5.176'
port = 30103

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect((host, port))

data_j = {"customer_name":"",
"serial_number":"406",
"parameter":["current_A","current_B","current_C"],
"limit":"1",
"start":"",
"end":""}

data_str = json.dumps(data_j)
# a = json.loads(data_str)
data_b = data_str.encode('utf-8')
# print(type(a))

tcp_client_socket.send(data_b)

resp = tcp_client_socket.recv(1024)
print(resp)
