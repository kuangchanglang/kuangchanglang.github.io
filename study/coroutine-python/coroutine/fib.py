def fib():
    first, second = 0, 1
    yield first

    while True:
        yield first + second
        first, second = second, first+second

if __name__ == '__main__':
    g = fib()
    for i in xrange(50):
        print g.next()
