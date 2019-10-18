# 使用socket连接上传数据

import socket
import json
import struct
import time


filename = 'data.txt'

#host = '45.32.14.94'
#port = 9200

host = '39.100.5.176'
port = 30102

tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client_socket.connect((host, port))

def timestamp_datatime(value):
    format = "%Y-%m-%d %H_%M_%S"
    value = time.localtime(value)
    dt = time.strftime(format, value)
    return dt

with open(filename, 'r') as f:
    data_r = f.read()
    data_j = json.loads(data_r)

for i in range(5):
    t = time.time()
    tf = timestamp_datatime(t)
    data_j['create_time'] = tf
    data_str = json.dumps(data_j)
    # a = json.loads(data_str)
    data_b = data_str.encode('utf-8')
    # print(type(a))

    #tcp_client_socket.send(struct.pack('i', len(data_b)) + data_b)
    tcp_client_socket.send(data_b)
    print('send: ', tf)
    time.sleep(1)
