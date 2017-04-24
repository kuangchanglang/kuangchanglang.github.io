#! /usr/bin/python
import sys
import time
from threading import Thread

def sleep():
    time.sleep(3)

def main():
    count = 2
    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    threads = {}
    for i in range(count):
        t = Thread(target=sleep)
        t.start()
        threads[i] = t

    for i in range(count):
        threads[i].join()

if __name__ == '__main__':
    main()
