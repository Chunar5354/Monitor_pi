import pymysql
from sql_helper import Helper
import threading
import logging

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/motor_server/motor.log', level=logging.DEBUG)


class Motor():
    def __init__(self):
        # instance into_db object
        self.db = Helper(host='',
                         user='Chunar',
                         password='chun.0927',
                         database='monitoring_test',
                         port=30106)
        self.db.connect()

    # reconnect to database
    def reconn_db(self):
        try:
            self.db.conn.ping()
        except:
            self.db.connect()

    def insert_data(self, data_dict):
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
                for value in value_list:
                    data_tuple = (create_time, value)
                    insert_datalist.append(data_tuple)
                sql = "INSERT INTO monitoring_test.{}(create_time, value) VALUES(%s, %s)".format(table_name)
                self.db.insert_many(sql, insert_datalist)

                #for value in value_list:
                #    sql = "INSERT INTO monitoring_Spike.{}(create_time, value) VALUES('{}', '{}')"\
                #        .format(table_name, create_time, value)
                #    self.db.insert(sql)

        except:
            logging.error('no data')
