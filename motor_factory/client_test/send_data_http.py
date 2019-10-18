# 使用request.post上传数据（没有响应值）

import requests
import json

#tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#tcp_client_socket.connect(("101.200.47.95", 9876))

filename = 'data.txt'

#url = 'http://101.200.47.95/Monitoring/php/api/api_insert_data.php'
url = 'http://39.100.5.176/Monitoring/php/new_api/api_insert_data.php'

with open(filename, 'r') as f:
    data_r = f.read()
    data_j = json.loads(data_r)

for i in range(15):
    data_j['create_time'] = '2019-9-28 14_47_{}'.format(str(i))
    data_str = json.dumps(data_j)

    response = requests.post(url, data=data_str).text
    print(response)
