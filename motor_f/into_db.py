import pymysql
from sql_helper import Helper


class Motor():
    def __init__(self):
        # instance into_db object
        self.db = Helper(host='',
                         user='VentoAureo',
                         password='GioGio114514',
                         database='monitoring_Spike',
                         port=3306)
        self.db.connect()

    def insert_data(self, data_dict):
        # insert data into database
        try:
            serial_number = data_dict.pop('serial_number')
            create_time = data_dict.pop('create_time')

            # insert data into every table
            for sub_name in data_dict.keys():
                table_name = serial_number + '_' + sub_name
                value_list = data_dict[sub_name].split('/')

                for value in value_list:
                    sql = "INSERT INTO monitoring_Spike.{}(create_time, value) VALUES('{}', '{}')"\
                        .format(table_name, create_time, value)
                    self.db.insert(sql)

        except:
            print('no data')
