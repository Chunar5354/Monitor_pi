接收树莓派上传的电机数据，并保存到数据库中

## 创建数据库

需要首先创建一个名为`raspberrypi`的数据库，并在其中创建相应的表

可以直接运行`make_db.txt`来创建：

进入mysql界面中，输入命令：
```
source ./make_db.txt;
```

## 程序逻辑

共有三个文件：

- 1.sql_helper.py：pymysql的封装文件，定义了一些mysql的操作函数
- 2.into_db.py：连接数据库，并运行数据插入sql命令
- 3.s_serve.py：使用socket开放服务器监听端口，接收数据并存入数据库

所以只需要在终端运行
```
python3 s_serve.py
```
