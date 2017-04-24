#! /usr/bin/python

import sys

num = 33

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

    for i in range(count):
        fib(num)

if __name__ == '__main__':
    #print fib(num)
    main()
