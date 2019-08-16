import pymysql
from sql_helper import Helper


class Motor():
    def __init__(self):
        # instance into_db object
        self.db = Helper(host='192.168.43.169',
                         user='Chunar',
                         password='chun.0927',
                         database='raspberrypi',
                         port=3306)
        self.db.connect()

    def insert_data(self, data_dict):
        # insert data into database
        try:
            # U, I, T, R
            for i in range(4):
                sql = "INSERT INTO {}(crt_time, value) VALUES('{}', '{}')"\
                    .format(data_dict["order"][i], data_dict["time"], data_dict["data"][i])
                self.db.insert(sql)

            # Vibration
            interval = int(1000 / len(data_dict["Vibration"]))
            print(interval)

            for i in range(len(data_dict["Vibration"])):
                vib_time = data_dict["time"] + '.' + str(interval * i)
                sql1 = "INSERT INTO Vibration(crt_time, value) VALUES('{}', '{}')"\
                    .format(vib_time, data_dict["Vibration"][i])
                self.db.insert(sql1)
        except:
            print('no data')
