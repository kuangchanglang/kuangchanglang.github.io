# coding=utf-8

import sys
import socket
import time
import gevent
from gevent import socket
from thread_server import handle_request

def server(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(500)
    while True:
        cli, addr = s.accept()
        gevent.spawn(handle_request, cli, gevent.sleep)

if __name__ == '__main__':
    server(8888)
