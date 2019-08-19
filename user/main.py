import sys
import pyqtgraph.pyqtgraph as pg
import array
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random
import numpy as np
import ADS1256
import RPi.GPIO as GPIO
import time
import wiringpi as wpi
import json
import socket
import struct
from iuv_get import Worker1
from r_get import Worker2
from t_get import Worker3

# 默认数据保存路径
save_path = 'data.txt'
vib_data = []


# 主窗口
class TabDemo(QWidget):
    def __init__(self, parent=None):
        super(TabDemo, self).__init__(parent)

        # 设置窗口标题与大小
        self.setWindowTitle('电机数据监测')
        self.setGeometry(5, 5, 1800, 950)

        # 数据传输
        self.timer = QTimer()
        try:
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM) #声明socket类型，同时生成链接对象
            print('trying')
            #self.client.connect(('192.168.43.139',9090)) #建立一个链接，连接服务器端的IP地址
            self.client.connect(('101.200.47.95',30002)) #建立一个链接，连接服务器端的IP地址
            self.timer.timeout.connect(self.Send_data)
            print('successfully connected')
        except:
            print('no valid connection')

        # 线程
        self.thread1 = Worker1() #电压与电流
        self.thread1.sinOut.connect(self.set_text)

        self.thread2 = Worker2() #转速
        self.thread2.sinOut.connect(self.set_rotate)

        self.thread3 = Worker3() #温度
        self.thread3.sinOut.connect(self.set_temp)

        #self.thread4 = Worker4() #振动
        #self.thread4.sinOut.connect(self.set_vibrate)

        # 绘图
        self.data1 = array.array('d')
        self.data2 = array.array('d')
        self.data3 = array.array('d')
        self.historyLength = 15
        self.vibLength = 1000

        self.p1 = pg.PlotWidget()
        self.p1.showGrid(x=True, y=True)
        self.p1.setRange(xRange=[0,self.historyLength], yRange=[5, 13], padding=0)
        self.p1.setLabel(axis='left', text='voltage / V')
        self.p1.setLabel(axis='bottom', text='x / point')
        self.p1.setTitle('电压')

        self.curve1 = self.p1.plot()
        self.curve1.setPen('r')

        # 电流图
        self.p2 = pg.PlotWidget()
        self.p2.showGrid(x=True, y=True)
        self.p2.setRange(xRange=[0,self.historyLength], yRange=[-1, 5], padding=0)
        self.p2.setLabel(axis='left', text='electricity / A')
        self.p2.setLabel(axis='bottom', text='x / point')
        self.p2.setTitle('电流')

        self.curve2 = self.p2.plot()
        self.curve2.setPen('g')

        # 振动图
        self.p3 = pg.PlotWidget()
        self.p3.showGrid(x=True, y=True)
        self.p3.setRange(xRange=[0,self.vibLength], yRange=[0, 3.3], padding=0)
        self.p3.setLabel(axis='left', text='vibration/g(m/s^2)')
        self.p3.setLabel(axis='bottom', text='x / point')
        self.p3.setTitle('振动')

        self.curve3 = self.p3.plot()
        self.curve3.setPen('y')

        # 初始化布局方式
        layout = QVBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()
        g1 = QGridLayout()
        v1 = QVBoxLayout()


        # 初始化按钮
        self.btn1 = QPushButton('     开 始     ')
        self.btn2 = QPushButton('     暂 停     ')
        self.btn3 = QPushButton('     恢 复     ')
        self.btn4 = QPushButton('设置文件保存路径')
        self.btn5 = QPushButton('振动数据保存路径')
        self.btn6 = QPushButton('     退 出     ')

        # 定义按钮的关联函数
        self.btn1.clicked.connect(self.Start)
        self.btn2.clicked.connect(self.Pause)
        self.btn3.clicked.connect(self.Restart)
        self.btn4.clicked.connect(self.Set_path)
        self.btn6.clicked.connect(self.QQuit)

        # 初始化标签与文本框
        label_title = QLabel('云计算智能电机监控演示系统')
        label_title.setFont(QFont("Roman times", 16, QFont.Bold))
        label_bottom = QLabel('大连理工大学     机械工程学院')
        label_bottom.setFont(QFont("Roman times", 14, QFont.Bold))
        label1 = QLabel('    电  压 ( V )     ')
        label2 = QLabel('    电  流 ( A )     ')
        label3 = QLabel('    温  度 ( ℃ )     ')
        label4 = QLabel('    转  速 ( r/min )   ')
        label5 = QLabel('    振  动 ( m/s^2 ) ')
        self.text1 = QLabel('                 ')
        self.text2 = QLabel('                 ')
        self.text3 = QLabel('                 ')
        self.text4 = QLabel('                 ')
        self.text5 = QLabel('                 ')

        # 设置标签文本居中
        label1.setAlignment(Qt.AlignCenter)
        label2.setAlignment(Qt.AlignCenter)
        label3.setAlignment(Qt.AlignCenter)
        label4.setAlignment(Qt.AlignCenter)
        label5.setAlignment(Qt.AlignCenter)
        label_title.setAlignment(Qt.AlignCenter)
        label_bottom.setAlignment(Qt.AlignCenter)
        self.text1.setAlignment(Qt.AlignCenter)
        self.text2.setAlignment(Qt.AlignCenter)
        self.text3.setAlignment(Qt.AlignCenter)
        self.text4.setAlignment(Qt.AlignCenter)
        self.text5.setAlignment(Qt.AlignCenter)

        # 温度计（使用QSlider滑块）
        self.sl1 = QSlider(Qt.Vertical)  # 设置为水平,垂直为Vertical
        self.sl1.setMinimum(0)  # 最小值
        self.sl1.setMaximum(100)  # 最大值
        self.sl1.setSingleStep(1)  # 设置步长
        self.sl1.setValue(25)  # 设置当前值
        # 设置刻度线位置，水平可以设置上下，垂直可以设置左右。或者两边
        self.sl1.setTickPosition(QSlider.TicksBelow)
        self.sl1.setTickInterval(5)  # 设置刻度间隔

        # 设置布局
        g1.addWidget(label1, 0, 0)
        g1.addWidget(self.text1, 0, 1)
        g1.addWidget(label2, 1, 0)
        g1.addWidget(self.text2, 1, 1)
        g1.addWidget(label3, 2, 0)
        g1.addWidget(self.text3, 2, 1)
        g1.addWidget(label4, 3, 0)
        g1.addWidget(self.text4, 3, 1)

        v1.addWidget(self.p1)
        v1.addWidget(self.p2)
        v1.addWidget(self.p3)

        h1.addLayout(v1)
        h1.addWidget(self.sl1)
        h1.addLayout(g1)

        h2.addWidget(self.btn1)
        h2.addWidget(self.btn2)
        h2.addWidget(self.btn3)

        h3.addWidget(self.btn4)
        h3.addWidget(self.btn5)
        h3.addWidget(self.btn6)

        layout.addWidget(label_title)  # 整体布局
        layout.addLayout(h1)
        layout.addLayout(h2)
        layout.addLayout(h3)
        layout.addWidget(label_bottom)

        # 显示布局
        self.setLayout(layout)

        # 使用QSS改变样式，主要是QSlider的样式
        self.qssStyle = '''
                    QSlider {
                    	background-color: rgba(220, 220, 220, 0.7);
                    	padding-top: 15px;
                    	padding-bottom: 15px;
                    	border-radius: 5px;
                    }
                    QSlider::add-page:vertical {
                    	background-color: rgb(225, 55, 57);
                    	width:5px;
                    	border-radius: 2px;
                    }
                    QSlider::sub-page:vertical {
                    	background-color: #7A7B79;
                    	width:5px;
                    	border-radius: 2px;
                    }
                    QSlider::handle:vertical {
                    	height: 14px;
                    	width: 14px;
                    	margin: 0px -3px 0px -3px;
                    	border-radius: 7px;
                    	background: white;
                    }
                    QLineEdit{
                    	background-color: rgba(220, 220, 220, 0.7);
                    	padding-top: 5px;
                    	padding-bottom: 5px;
                    	border-radius: 5px;
                        font: 75 16pt "Roman times";
                        font-size:16px;
                    }
                    QLabel{
                    	background-color: rgba(220, 220, 220, 0.7);
                        padding-top: 5px;
                    	padding-bottom: 5px;
                    	border-radius: 5px;
                        font: 75 16pt "Roman times";
                        font-size:36px;
                    }
                            '''
        self.setStyleSheet(self.qssStyle)

        self.vib_list = []  # 振动数据列表
        # 创建一个字典存放数据，用于json格式的文本写入
        self.data_dict = {} #本地保存的数据
        self.data_send = {"time":"no time", "order":["U", "I", "T", "R"], "id":"raspberrypi", "data":{}} #最终发送的数据
        self.sub_send = {}  # 发送数据的子字典，用于存放除了振动的其他数据
        self.key_num = 0

        # 用于存储的全局温度和转速变量
        self.w_temp = 0
        self.w_rotate = 0

    # 开始按钮事件
    def Start(self):
        self.thread1.start()
        self.thread2.start()
        self.thread3.start()
        #self.thread4.start()
        self.timer.start(1000)

    # 暂停按钮事件
    def Pause(self):
        self.thread1.working = False

    # 恢复按钮事件
    def Restart(self):
        self.thread1.working = True
        self.thread1.start()

    # 显示温度
    def set_temp(self, temp):
        self.text3.setText(str(temp)) #温度
        self.sl1.setValue(temp)
        self.w_temp = temp

    # 振动
    def set_vibrate(self, timer):
        timer.start(1)

    # 显示电压、电流、振动数据，并保存和画图
    def set_text(self, data_list):
        global save_path, vib_data

        vol = data_list[0]  # float数据
        ele = data_list[1]
        vib_list = data_list.pop(2)
        self.text1.setText(str(vol))  # 电压
        self.text2.setText(str(ele))  # 电流


        # 绘制图像
        # 电压
        if len(self.data1)<self.historyLength:
            self.data1.append(vol)
        else:
            self.data1[:-1] = self.data1[1:]
            self.data1[-1] = vol
        self.curve1.setData(np.frombuffer(self.data1, dtype=np.double))

        # 电流
        if len(self.data2)<self.historyLength:
            self.data2.append(ele)
        else:
            self.data2[:-1] = self.data2[1:]
            self.data2[-1] = ele
        self.curve2.setData(np.frombuffer(self.data2, dtype=np.double))

        # 振动
        vib_all = 0
        vib_send = []  # 这个列表存放减掉平均值后的振动数据
        for i in range(len(vib_list)):
            vib_all += vib_list[i]

        vib_aver = vib_all/len(vib_list)

        for i in range(len(vib_list)):
            vib_send.append(round(vib_list[i]-vib_aver, 4))

        if len(self.data3)<self.vibLength:
            for i in range(len(vib_list)):
                self.data3.append(round(vib_list[i]-vib_aver, 4))
        else:
            for i in range(len(vib_list)):
                self.data3[:-1] = self.data3[1:]
                self.data3[-1] = round(vib_list[i]-vib_aver, 4)

        self.curve3.setData(np.frombuffer(self.data3, dtype=np.double))

        # 将温度和转速数据存到列表中
        data_list.append(self.w_temp)
        data_list.append(self.w_rotate)

        # 将数据存入字典 以及发送
        self.data_dict[self.key_num] = data_list
        self.data_dict["Vibration"] = vib_send
        self.data_send["data"] = data_list  # 要发送的数据
        self.data_send["Vibration"] = vib_send
        self.key_num += 1
        vib_data = []  # 每次保存字典之后将振动数据清空

        with open(save_path, 'w') as f:
            # 文件写入格式为json字符串，先将字典编码成json格式然后写入
            json_w = json.dumps(self.data_dict)
            f.write(json_w)

    # 显示转速
    def set_rotate(self, rotate):
        self.text4.setText(str(rotate))
        self.w_rotate = rotate

    # 设置数据保存路径
    def Set_path(self):
        global save_path
        text, ok = QInputDialog.getText(self, '设置数据存储路径', '请输入路径：')  # 对话框
        if ok:
            save_path = text

    # 使用socket发送数据
    def Send_data(self):
        if self.data_send["data"] == []:
            print('empty')
            pass
        else:
            now_time = int(time.time())
            time_unix = self.timestamp_datatime(now_time)
            self.data_send["time"] = time_unix
            msg = json.dumps(self.data_send).encode('utf-8')  # 将字典转化为json字符串，再转换成字节串
            
<<<<<<< HEAD
            self.client.send(struct.pack('i', len(msg)) + msg)   # 发送4字节的数据长度+数据内容
=======
            self.client.send(struct.pack('i', len(msg)) + msg)   # 发送2字节的数据长度+数据内容
>>>>>>> b073cd42f975eb0f749ac9c7d762fc05c16c2843
            self.data_send = {"time":"no time", "order":["U", "I", "T", "R"], "id":"raspberrypi", "data":{}}  # 每次发送后重置字典
            self.sub_send = {}  # 发送后清空

    # 转换 unix 时间戳
    def timestamp_datatime(self, value):
        format = "%Y-%m-%d %H:%M:%S"
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt

    # 退出按钮关联事件
    def QQuit(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = TabDemo()
    demo.show()
    sys.exit(app.exec_())
