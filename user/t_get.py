import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import time

# 温度采集线程
class Worker3(QThread):
    sinOut = pyqtSignal(float)

    def __init__(self, parent = None):
        super(Worker3, self).__init__(parent)

        # DS18B20文件的地址
        self.add = '/sys/bus/w1/devices/28-0118793b97ff/w1_slave'

        self.working = True
        self.num = 0

    def __def__(self):
        self.working = False
        self.wait()

    def Get_temp(self):
        try:  # 读取DS18B20文件，并解析得到温度值
            with open(self.add, 'r') as f:
                lines = f.readlines()
            num_list = lines[1].split('=')
            num_str = num_list[1]
            num = float(num_str)
            temp = num/1000
        except:
            temp = 0
            print('no right ds18b20')
        return temp

    def run(self):
        while self.working == True:
            temp = round(self.Get_temp(), 2)

            self.sinOut.emit(temp)
            time.sleep(0.1)
