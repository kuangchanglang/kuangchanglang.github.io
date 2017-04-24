# coding=utf-8

import time
from greenlet import greenlet

def foo():
    return 0

def main():
    i = 0
    try :
        while True:
            g = greenlet(foo)
            g.switch()
            i+=1
    except:
        pass
    finally:
        print 'i=%d' % i


if __name__ == '__main__':
    main()
