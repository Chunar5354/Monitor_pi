import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import RPi.GPIO as GPIO
import time
import wiringpi as wpi


# 转速采集线程
class Worker2(QThread):
    sinOut = pyqtSignal(float)

    def __init__(self, parent = None):
        super(Worker2, self).__init__(parent)

        self.r_pin = 21  # 转速传感器数据输入引脚
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.r_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # 设置GPIO为上拉电阻输入模式

        self.num = 20  # 设置计算多少圈的平均值，越大数据越准确，耗时越长

        self.working = True

    def __def__(self):
        self.working = False
        self.wait()

    def run(self):
        while self.working == True:
            r_ft = wpi.micros()

            for i in range(self.num):
                while GPIO.input(self.r_pin):
                    pass
                while GPIO.input(self.r_pin) == 0:
                    pass
                print(i)

            t = wpi.micros()-r_ft
            v = 1000000*(self.num-1)/t*60  # 每分钟的转速
            v = round(v, 2)

            self.sinOut.emit(v)
            time.sleep(0.2)
