## 文件说明

根目录下的几个txt文件为操作mysql的文件，用于批量增删一些数据

### upload_data_server

硬件端上传数据的服务器程序，主程序为`upload_server.py`，后台运行即可开启socket监听服务

硬件端上传的数据格式见`/client_server/data.txt`

### overview

用于读取数据的用户总览界面，主程序为`overview_web_server.py`(websocket网页端)，以及`overview_soc_server.py`(socket手机APP端)，后台运行即可开启相应服务

overview目录下的`fetch_aver_thread.py`是从mysql中获取数据的多线程版本

客户端发送请求的数据为json格式，见`/overview/data_format.json`

### fetch_data_server

用于客户端读取数据，主程序为`websocket_server.py`(websocket网页端)，以及`socket_server.py`(socket手机APP端)，后台运行即可开启相应服务

客户端发送请求的格式与overview相同

### client_test

上传以及读取数据的测试文件，具体功能见文件内注释
