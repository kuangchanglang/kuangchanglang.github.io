#!/usr/bin/python
# encoding : utf-8

import os
from flup.server.fcgi import WSGIServer

count = 0
def myapp(environ, start_response):
    global count
    start_response('200 OK', [('Content-Type', 'text/plain')])
    count += 1
    return ['Hello World fastcgi!\nAccess count %d\n Running pid: %d' % (count, os.getpid())]

if __name__  == '__main__':
   WSGIServer(myapp, bindAddress=('127.0.0.1',8080)).run()
