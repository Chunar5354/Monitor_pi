# Use pymysql and pandas to fetch data

import pymysql
import pandas as pd
import numpy as np
import threading


class Hunter():
	def __init__(self):
		# every parameter has a different number during one second
		self.limit_dict = {'current_A': '250',
						   'current_B': '250',
						   'current_C': '250',
						   'voltage_AB': '250',
						   'voltage_BC': '250',
						   'voltage_CA': '250',
						   'temp_fore_winding_A': '5',
						   'temp_fore_winding_B': '5',
						   'temp_fore_winding_C': '5',
						   'temp_fore_bearing': '5',
						   'temp_rear_bearing': '5',
						   'temp_water': '5',
						   'temp_rotator': '5',
						   'temp_controller_env': '5',
						   'rev': '120',
						   'vib_fore_bearing': '1000',
						   'vib_rear_bearing': '1000',
						  }
		# set a global dict to receive the result in threads
		self.result_dict = {}
		self.crt_time = None

		# users can choose fetch average or single data
		# self.fetch_aver=0: single, self.fetch_aver=1: average
		self.fetch_aver = 0
	
	# get average value, use as multithread
	def _dataaver(self, para, sql):
		'''
		get average data from database
		'''
		# pymysql must create a new connection for every threading
		db = pymysql.connect(host='',
							user='Chunar',
							password='chun.0927',
							database='monitoring_Spike',
							port=30106)
		result = pd.read_sql(sql, db)  # method from dandas, read mysql into pandas.dataframe
	
		# get time
		if self.crt_time == None:
			self.crt_time = str(result['create_time'][1]).split('.')[0]

		# use mean method to calculate average
		# value_aver = round(result['value'].mean(), 2)
		value_aver = result['value'][0]
		self.result_dict[para] = value_aver	

	# get the first value in the giving interval
	def _datasingle(self, para, sql):
		'''
		get the first data in the giving interval
		'''
		# do connection, pymysql must create a new connection for every threading
		db = pymysql.connect(host='',
							user='Chunar',
							password='chun.0927',
							database='monitoring_Spike',
							port=30106)
		cur = db.cursor()

		# fetch data
		count = cur.execute(sql)
		if count != 0:
			dataall = cur.fetchall()

		# get time
		if self.crt_time == None:
			self.crt_time = str(dataall[0][0]).split('.')[0]

		# get single value
		result_value = dataall[0][1]
		self.result_dict[para] = result_value

	# main get data
	def get_data(self, data_dict):
		'''
		para: a dictioinary by the format shown in file data_formai.json
		return: a dictionary include create_time and all the value of giving parameter
		'''
		# clear global variable
		self.result_dict = {}
		self.crt_time = None

		start_time = data_dict["start"]
		end_time = data_dict["end"]
		para_list = data_dict["parameter"]
		th_list = []

		# fetch average or single, depends on the value of self.fetch_aver
		for para in para_list:
			# fetch every average of parameters
			if self.fetch_aver == 1:
				# if start_time is not null, means fetching historial data, between start and end
				if len(start_time) > 1:
					sql = "select create_time, value from monitoring_Spike.406_{} where create_time>'{}' && create_time<'{}'".format(para, start_time, end_time)
				# if strat_time is null, means fetching the newets data
				else:
					sql = "select create_time, value from monitoring_Spike.406_{} order by create_time desc limit {}".format(para, self.limit_dict[para])
				# put all threadings in a list
				th_list.append(threading.Thread(target=self._dataout, args=(para, sql)))

			# fetch the first value in every parameter
			else:
				# if start_time is not null, means fetching historial data, between start and end
				if len(start_time) > 1:
					sql = "select create_time, value from monitoring_Spike.406_{} where create_time>'{}' && create_time<'{}' limit 1".format(para, start_time, end_time)
				# if strat_time is null, means fetching the newets data
				else:
					sql = "select create_time, value from monitoring_Spike.406_{} order by create_time desc limit 1".format(para)
				# put all threadings in a list
				th_list.append(threading.Thread(target=self._datasingle, args=(para, sql)))

		# start threadings
		for th in th_list:
			th.start()
		# use join method to wait until every threading is finished
		for th in th_list:
			th.join()

		# add time in result_dict
		self.result_dict["create_time"] = str(self.crt_time)
		result_dict = self.result_dict
		return result_dict
		
