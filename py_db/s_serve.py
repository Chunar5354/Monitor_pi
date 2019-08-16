import socket
import pymysql
import json
from into_db import Motor

# define connection parameters
host = '192.168.43.169'
port = 9090

# connect via socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create a socket object, and declare the type
server.bind((host, port))  # connect with ip and port
server.listen(5)  # start to listen, and there can be 5 connections in queue

# instance a Motor object
mt = Motor()

while True:
    conn, addr = server.accept()  # conn is a new socket object, to deal with communication
    print(conn, addr)

    while True:
        data = conn.recv(1024)  # rceive 1024 bytes data as most
        print(type(data))  # show the type of the data received

        # Translate byte data into dictionary
        data_dict = json.loads(data.decode())

        # insert data into database
        mt.insert_data(data_dict)

        # check
        print('recive:', data.decode())  # decode the data and print
        conn.send(data.upper())  # send data back

    conn.close()