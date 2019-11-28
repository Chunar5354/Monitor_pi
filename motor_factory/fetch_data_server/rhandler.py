import redis

class RedisHandler():
	'''
	Contains methods of inserting and fetching data from redis

	Attributes:
		pool: redis connection pool
		limit_dict: show the number for every data in one minute
	'''
	def __init__(self, host='localhost', port=6379, password='redi.0927', db=0):
		self.pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
		self.limit_dict = {'temp_water': 5,
						   'temp_rotator': 5,
						   'current_A': 250,
						   'current_B': 250,
						   'current_C': 250,
						   'voltage_AB': 250,
						   'voltage_BC': 250,
						   'voltage_CA': 250,
						   'temp_fore_winding_A': 5,
						   'temp_fore_winding_B': 5,
						   'temp_fore_winding_C': 5,
						   'temp_fore_bearing': 5,
						   'temp_rear_bearing': 5,
						   'temp_controller_env': 5,
						   'rev': 120,
						   'vib_fore_bearing': 1000,
						   'vib_rear_bearing': 1000,
						  }

	def inhash(self, data_dict):
		'''
		Insert data into redis database as hash

		Args:
			data_dict: {para: value} to insert into redis, both key and value are string type
		'''
		# Create a connection from connection pool
		conn = redis.Redis(connection_pool=self.pool)
		# try:
		serial_number = data_dict.pop('serial_number')
		create_time = data_dict.pop('create_time').replace('_', ':')

		# Data struct is: create_time: {table: value}, all of them are string type
		# but when they are insert into redis, thrie type will be bytes
		for sub_name in data_dict.keys():
			table_name = serial_number + '_' + sub_name
			conn.hset(create_time, table_name, data_dict[sub_name][:-1])  # delete '/n' in the end

			# conn.expire(create_time, 300)  # set expire time, the number stands for seconds
		# except:
		# 	print('data error')

	def outhash(self, data_dict):
		'''
		Fetch data from redis hash, then format the data

		Args:
			data_dict: a dictionary contains information od users

		Returns:
			result_dict: target data user want to get, as a dictionary
		'''
		conn = redis.Redis(connection_pool=self.pool)
		serial_number = data_dict["serial_number"]
		start_time = data_dict["start"]
		end_time = data_dict["end"]
		para_list = data_dict["parameter"]

		result_dict = {}
		for para in para_list:
			# if user require data time, use it
			if len(start_time) > 1:
				result_dict[para] = conn.hget(strat_time, serial_number + para)

			# id user does not require data time, fetch the newest data
			else:
				# every data getting from redis is bytes type
				crt_time = max(conn.keys()).decode()
				# print(crt_time)
				result_data = conn.hget(crt_time, serial_number + '_' + para).decode()
				result_list = result_data.split('/')
				# format data as a list, add decimal part into crt_time
				value_list = [[crt_time + '.' + str(int(1000 / self.limit_dict[para] * i)), result_list[i]] for i in range(len(result_list))]
				result_dict[para] = value_list
		# print('from redis')
		return result_dict
	
