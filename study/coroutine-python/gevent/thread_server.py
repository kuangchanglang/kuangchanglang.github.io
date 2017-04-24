# coding=utf-8
import sys
import socket
import time
import threading

def threads(port):
    s = socket.socket()
    s.bind(('0.0.0.0', port))
    s.listen(3000)
    while True:
        try:
            cli, addr = s.accept()
            t = threading.Thread(target=handle_request, args=(cli, time.sleep))
            #t.daemon = True
            t.start()
        except:
            # cli.shutdown(socket.SHUT_WR)
            s.close()
            return

def handle_request(s, sleep):
    try:
        s.recv(1024)
        sleep(3)
        s.sendall('http/1.0 200 OK\n\nHello World! ''')
        s.shutdown(socket.SHUT_WR)
        print '.',
    except Exception, ex:
        print ex
    finally:
        sys.stdout.flush()
        s.close()

if __name__ == '__main__':
    threads(9998)
