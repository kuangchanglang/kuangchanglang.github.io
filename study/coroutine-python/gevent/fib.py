import gevent
import random

def task():
    """
    Some non-deterministic task
    """
    print 'sleep start'
    gevent.sleep(0.1)
    print 'sleep done'

def fib(n):
    if n <= 0:
        return 0
    if n < 2:
        return 1

    return fib(n-1) + fib(n-2)

def cal():
    print 'fib start'
    fib(33)
    print 'fib done'

gevent.joinall([
gevent.spawn(task),
gevent.spawn(cal),
])
