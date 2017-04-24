#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

import os
print "Content-Type: text/plain;charset=utf-8"
print

print "Hello World!\n Running pid: %d" % os.getpid()
