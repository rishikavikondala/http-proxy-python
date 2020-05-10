#!/usr/bin/env python3

import socket
import sys
import time

def main():
    HOST = '127.0.0.1'
    PORT = int(sys.argv[1])
    FILE = sys.argv[2]
    MODE = 'LINE'

    if len(sys.argv) == 4:
        MODE = 'CHUNK'
        CHUNK = int(sys.argv[3])

    print('Connecting to port {}'.format(PORT))
    print('Sending message in {} mode'.format(MODE))
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if MODE == 'LINE':
            with open(FILE, 'r') as input:
                for line in input:
                    line = line[:-1] + '\r\n'
                    s.sendall(line.encode('iso-8859-1'))
                    time.sleep(1)
        else:
            with open(FILE, 'rb') as input:
                if CHUNK == 0:
                    data = input.read()
                    s.sendall(data)
                else:
                    data = input.read(CHUNK)
                    while data != b'':
                        s.sendall(data)
                        data = input.read(CHUNK)
                        time.sleep(1)

if __name__ == '__main__':
    main()