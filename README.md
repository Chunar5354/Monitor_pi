树莓派采集电机参数并显示与上传程序

要采集的参数有：电压、电流、转速、温度、振动

## 数据采集

采用多线程的方式采集数据
- `iuv_get.py`线程一，通过ADS1256采集电压、电流和振动数据
- `r_get.py`线程二，通过计数方式采集转速数据
- `t_get.py`线程三，通过树莓派内置的单总线方式读取DS18B20传感器来获取温度值

## 数据显示

图形界面使用`PYQT5`编写，图像绘制使用`pyqtgraph`扩展库

PYQT5安装：
```
sudo apt-get install python3-pyqt5
```

pyqtgraph获取：
```
git clone https://github.com/pyqtgraph/pyqtgraph
python setup.py install
```

## 数据上传

数据上传使用`socket`模块实现

## 其它文件

还需要额外安装一个树莓派的硬件操作库`wiringpi`
```
pip install wiringpi     // 有多版本python的话尝试: pip3 install wiringpi
```

`config.py`与`ADS1256.py`为ADS1256硬件配置文件
