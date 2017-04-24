#! /usr/bin/python

from greenlet import greenlet
import sys

num = 30
grs = []

def fib(n):
    if n <= 0:
        return 0
    if n < 2:
        return 1

    return fib(n-1) + fib(n-2)

def main():
    global grs
    count = 2
    if len(sys.argv) > 1:
        count = int(sys.argv[1])

    for i in range(count):
        grs.append(greenlet(fib))

    for i in range(count):
        grs[i].switch(num)

if __name__ == '__main__':
    #print fib(num)
    main()
