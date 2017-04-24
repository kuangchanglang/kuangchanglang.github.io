#!/bin/python
# coding=utf-8

#from wsgiref.simple_server import make_server
from myserver import make_server
from myapp import application

httpd = make_server('', 8080, application)
print "Serving HTTP on port 8080..."
httpd.serve_forever()
