import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import ADS1256
import time


# 电压、电流以及振动采集线程
class Worker1(QThread):
    sinOut = pyqtSignal(list)  # 传出信号，括号中为参数类型

    def __init__(self, parent = None):
        super(Worker1, self).__init__(parent)

        # 初始化ADC
        self.ADC = ADS1256.ADS1256()
        self.ADC.ADS1256_init()

        self.working = True
        self.num = 0

    def __def__(self):
        self.working = False
        self.wait()

    # 多次采集计算平均值来提高准确度
    def Get_adc(self):
        ch0_list = []  # U
        ch1_list = []  # I
        ch2_list = []  # Vibration
        for i in range(10):
            ch0 = self.ADC.ADS1256_GetVibrate(2)*5.0/0x7fffff
            ch0_list.append(ch0)
        for i in range(10):
            ch1 = self.ADC.ADS1256_GetVibrate(0)*5.0/0x7fffff
            ch1_list.append(ch1)
        for i in range(50):
            ch2 = self.ADC.ADS1256_GetChannalValue(1)*5.0/0x7fffff  # 振动
            ch2 = ch2*20
            ch2 = round(ch2, 2)
            ch2_list.append(ch2)
        return ch0_list, ch1_list, ch2_list

    def Get_value(self):
        ch0_all = 0
        ch1_all = 0
        ch0_list, ch1_list, ch2_list = self.Get_adc()
        ch0_list.sort()
        ch1_list.sort()

        # 除去最大和最小值，计算平均
        for i in range(8):
            ch0_all += ch0_list[i+1]
            ch1_all += ch1_list[i+1]
        ch0 = ch0_all/8
        ch1 = ch1_all/8
        vol = ch0*4

        ele = (ch1-2.6)/0.185  # 电流传感器的计算方法
        vol = round(vol, 2)
        ele = round(ele, 2)
        return vol, ele, ch2_list

    def run(self):
        while self.working == True:
            vol, ele, ch2_list = self.Get_value()
            list_w = [vol, ele, ch2_list]
            self.sinOut.emit(list_w)  # 将数据列表传递出去
            time.sleep(0.2)
