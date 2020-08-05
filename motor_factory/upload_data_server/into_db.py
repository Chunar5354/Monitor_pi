import pymysql
import threading
import logging

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/upload_data_server/upload.log', level=logging.DEBUG)


class Motor():
	'''
	Insert data into mysql
	Attributes:
		conn: pymysql connection object
		cur: pymysql object, handle concrete action
	'''
	def __init__(self):
		# instance into_db object
		self.conn = pymysql.connect(host='',
						 		  user='Chunar',
						 		  password='chun.0927',
								  database='monitoring_test',
								  port=30106)
		self.cur = self.conn.cursor()

	# reconnect to database
	def reconn_db(self):
		'''
		For every database action, firstly need to test the connection, and reconnect
		'''
		try:
			self.conn.ping()
		except:
			self.__init__()
	
	def _insert_many(self, sql, datalist):
		'''
		Using executemany() method to insert a list into mysql
		Args:
			sql: sql string
			datalist: a list which elements like (create_time, value)
		Returns:
			count: the number of operating lines
		'''
		count = 0
		try:
			count = self.cur.executemany(sql, datalist)
			self.conn.commit()
		except Exception as ex:
			logging.error(ex)
		return count
		

	def insert_data(self, data_dict):
		'''
		Format the received data, then insert it into database
		Args:
			data_dict: received data
		'''
		self.reconn_db()
		# insert data into database
		try:
			serial_number = data_dict.pop('serial_number')
			create_time = data_dict.pop('create_time')

			# insert data into every table
			for sub_name in data_dict.keys():
				table_name = serial_number + '_' + sub_name
				value_list = data_dict[sub_name].split('/')
				insert_datalist = []
				for value in value_list[:-1]:
					data_tuple = (create_time, value)
					insert_datalist.append(data_tuple)
				sql = "INSERT INTO monitoring_test.{}(create_time, value) VALUES(%s, %s)".format(table_name)
				count = self._insert_many(sql, insert_datalist)

		except:
			logging.error('no data')
