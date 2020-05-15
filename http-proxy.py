#!/usr/bin/env python3

# add import statements here
import argparse
import json
import socket

# define classes, enums, etc here

# define functions here
def parse_message(data):
    # initialize empty dictionary
    message = {}

    length, raw_request = get_request(data)
    parsed_request = raw_request.split(' ')

    # parse bytes and assign key / value pairs
    message['method'] = parsed_request[0] # HTTP method name such as GET
    message['uri'] = parsed_request[1] # request_partsaddress or resource name from the request, such as www.uw.edu
    message['version'] = parsed_request[2] # HTTP version such as HTTP/1.0
    message['headers'] = parse_headers(length, data) # List of headers

    # If parsing is successful, return a completed message (if applicable) and unused bytes
    return message, None

    # If parsing fails, return the entire buffer and an indicator that parsing was incomplete
    return None, data

def get_request(data):
    raw_req = data.decode('utf-8')
    split_req = raw_req.partition('\n')
    return len(split_req[0]), split_req[0].strip()

def parse_headers(index, data):
    data = data[index+1:].decode('utf-8')
    raw_headers = data.split('\n')
    parsed_headers = {}
    for i in range(len(raw_headers)):
        this_header = raw_headers[i].split(':')
        parsed_headers[this_header[0].strip()] = this_header[1].strip()
    return parsed_headers

def main():
    # register arguments 
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, help='TCP port for HTTP proxy', default=9999)

    # parse the command line
    args = parser.parse_args()

    # Set host and port
    HOST_ADDRESS = '127.0.0.1'
    PORT_NUMBER = args.port

    # Accept new connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST_ADDRESS, PORT_NUMBER))
        s.listen()
        buffer = b''
        while True:
            conn, addr = s.accept()
            with conn:
                message, unused = parse_message(buffer)
                # Connection Source: \<IP address returned from the call to Socket.accept()>
                print(message['method'])
                print(message['uri'])
                print(message['headers'])

    # data = b'GET http://neverssl.com/ HTTP/1.1\nHost: neverssl.com\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\nAccept-Encoding: gzip, deflate, br\nAccept-Language: en-US,en;q=0.9'
    # length, req = get_request(data)
    # print(req)
    # print(parse_headers(length, data))

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()