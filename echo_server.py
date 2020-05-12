#!/usr/bin/env python3

import argparse
import json
# add additional import statements here
import socket

def get_simple_response(message):
    return message

def get_hello_response(message):
    return 'Hello, ' + message

def get_request_response(message):
    # TODO: Parse request line of standard HTTP request
    elements = message.split()
    if len(elements) != 3:
        return "Invalid HTTP Request Line"
    request = { 'method': elements[0], 'path': elements[1], 'version': elements[2]}
    return json.dumps(request) # converts dictionary to JSON string

def get_header_response(message):
    # TODO: Parse header line of standard HTTP request
    elements = message.split(':')
    if len(elements) != 2:
        return "Invalid HTTP Header Line"
    header = { 'name': elements[0], 'value': elements[1] }
    return json.dumps(header) # converts dictionary to JSON string

def main():
    # more argument parsing examples at https://realpython.com/command-line-interfaces-python-argparse/

    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port of Echo Server', default=9999)
    parser.add_argument('-m', '--mode', choices=['simple', 'hello', 'request', 'header'], default='simple')
    # parser.add_argument('text', type=str, help='UTF-8 text to send to echo server')

    # parse the command line
    args = parser.parse_args()

    HOST_ADDRESS = '127.0.0.1'
    PORT_NUMBER = args.port

    # examine the input
    # print(args.port)
    # print(args.text)
    # print(args.text.encode('utf-8'))
    # print(args.text.encode('utf-8').hex())

    # SET UP SERVER SOCKET
    # Use sockopt to avoid bind() exception: OSError: [Errno 48] Address already in use

    # ACCEPT NEW CONNECTIONS (in a loop / one at a time)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST_ADDRESS, PORT_NUMBER))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by: ', addr)
                message = conn.recv(4096)
                decoded = message.decode('utf-8') # RECEIVE BYTES AND DECODE AS STRING
                if args.mode == 'simple':
                    response = get_simple_response(decoded)
                elif args.mode == 'hello':
                    response = get_hello_response(decoded)
                elif args.mode == 'request':
                    response = get_request_response(decoded)
                elif args.mode == 'header':
                    response = get_header_response(decoded)
                conn.sendall(response.encode('utf-8'))

        # ENCODE STRING TO BYTES USING UTF-8 AND SEND RESPONSE TO CLIENT

        # CLOSE CONNECTION TO CLIENT BUT KEEP SERVER SOCKET OPEN

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()