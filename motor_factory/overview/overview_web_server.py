# Websocket server using tornado
import tornado
import tornado.websocket
from fetch_aver import Hunter
import logging
import json
import time
from simu_overview import data_magic

logging.basicConfig(filename='/home/Chunar/codes/Monitor_pi/motor_factory/overview/overview.log', level=logging.DEBUG)

class EchoWebSocket(tornado.websocket.WebSocketHandler):

    # rewrite this methos so that the connection can allow all address
    def check_origin(self, origin):
        return True

    # while start a new connection, log the time
    def open(self):
        t = time.localtime()
        logging.info('Websocket served at time: {}'.format(time.asctime(t)))

    # deal with data fetching
    def on_message(self, message):
        data = message

        # translate data format into dictionary
        data_dict = json.loads(data)

        # get result
        ht = Hunter()
        result_dict = ht.get_data(data_dict) 
        # simulate voltage data for exhibition, in peacetime, annotate it
        # result_dict = data_magic(result_dict)

        data_send = json.dumps(result_dict)  # translate into str to send

        self.write_message(data_send)

    def on_close(self):
        logging.info('*'*10 + 'WebSocket closed' + '*'*10)


if __name__=='__main__':
    app = tornado.web.Application([
        (r'/', EchoWebSocket),
    ])
    app.listen(30104)  # set the port, the url will be "ws://ip:30104"
    tornado.ioloop.IOLoop.current().start()
