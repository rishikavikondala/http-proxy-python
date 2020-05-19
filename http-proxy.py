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

    length, raw_request = get_fields(data)
    parsed_request = raw_request.split(' ', 2)

    # parse bytes and assign key / value pairs
    message['method'] = parsed_request[0] # HTTP method name such as GET
    message['uri'] = parsed_request[1] # request_parts address or resource name from the request, such as www.uw.edu
    message['version'] = parsed_request[2] # HTTP version such as HTTP/1.0
    try:
        message['headers'] = parse_headers(length, data) # List of headers
        # If parsing is successful, return a completed message (if applicable) and unused bytes
        return message, None
    except:
        # If parsing fails, return the entire buffer and an indicator that parsing was incomplete
        return None, data

def get_fields(data):
    raw_req = data.decode('utf-8')
    split_req = raw_req.partition('\n')
    return len(split_req[0]), split_req[0].strip()

def parse_line(data, encoding = 'iso-8859-1'):
    fields = data.partition('\n')
    if len(fields[1]) == 0:
        return None, data
    line = fields[0].rstrip('\r')
    if len(fields[2]) == 0:
        return line, None
    return line, fields[2]

def parse_headers(index, data):
    headers = {}
    data = data[index+1:].decode('iso-8859-1')
    line, unparsed = parse_line(data)
    while line != '':
        if line is None:
            raise Exception
        else:
            parts = line.split(':')
            headers[parts[0]] = parts[1].strip()
        line, unparsed = parse_line(unparsed)
    return headers    

def print_summary(message,  address):
    print("Connection source: " + address)
    print("HTTP method: " + message['method'])
    print("Destination: " + message['uri'])
    print("Headers: ")
    print(message['headers'])

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
        while True:
            conn, addr = s.accept()
            with conn:
                buffer = b''
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    buffer = buffer + data
            parsed_message, remainder = parse_message(buffer)
            print_summary(parsed_message, addr[0])

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()