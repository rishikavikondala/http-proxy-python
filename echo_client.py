#!/usr/bin/env python3

import argparse
# add additional import statements here
import socket

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port of Echo Server', default=9999)
    parser.add_argument('text', type=str, help='UTF-8 text to send to echo server')

    # parse the command line
    args = parser.parse_args()
    message = args.text

    HOST_ADDRESS = '127.0.0.1'
    PORT_NUMBER = args.port

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST_ADDRESS, PORT_NUMBER))
        s.sendall(message.encode())
        print('INPUT: {}'.format(s.recv(4096)))

    # ESTABLISH SOCKET AND CLIENT CONNECTION
    # SEND MESSAGE
    # RECEIVE RESPONSE

    # EXAMINE RESPONSE
    # print('INPUT: {}'.format(message))
    # print('RESPONSE: {}'.format(response))
    # print('UTF-8 ENCODING: {}'.format(response)) # Encode response as UTF-8

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()