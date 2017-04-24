#! /usr/bin/python
from threading import Thread
import sys

num = 30

def fib(n):
    if n <= 0:
        return 0
    if n < 2:
        return 1

    return fib(n-1) + fib(n-2)

def main():
    count = 2
    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    threads = {}
    for i in range(count):
        t = Thread(target=fib, args=(num,))
        t.start()
        threads[i] = t

    for i in range(count):
        threads[i].join()

if __name__ == '__main__':
    print fib(num)
    main()
