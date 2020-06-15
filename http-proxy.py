#!/usr/bin/env python3

import argparse
import json
import socket
from urllib.parse import urlparse
from enum import Enum, auto

# Enumeration to represent message types 
class MessageType(Enum):
    REQUEST = auto() # constant values are auto-assigned
    RESPONSE = auto() # constant values are auto-assigned

# Gets fields from first line of request/response
def get_fields(data):
    raw_req = data.decode('utf-8')
    split_req = raw_req.partition('\n')
    return len(split_req[0]), split_req[0].strip()

# Parses one line of an http request/response
def parse_line(data, encoding = 'iso-8859-1'):
    fields = data.partition('\n')
    if len(fields[1]) == 0:
        return None, data
    line = fields[0].rstrip('\r')
    if len(fields[2]) == 0:
        return line, None
    return line, fields[2]

# Populates http headers into a dictionary
def parse_headers(index, data, method):
    headers = {}
    data = data[index+1:].decode('iso-8859-1')
    line, unparsed = parse_line(data)
    content_length = None
    body = b''
    while line != '':
        if line is None:
            raise Exception
        else:
            parts = line.split(':')
            headers[parts[0]] = parts[1].strip()
            if parts[0] == 'Content-Length':
                content_length = int(parts[1].strip())
        line, unparsed = parse_line(unparsed)
    if content_length is not None and method != 'GET':
        body = unparsed[0: content_length]
    return headers, content_length, body

def parse_message(data, message_type):
    if message_type is MessageType.REQUEST:
        message = {}
        length, raw_request = get_fields(data)
        parsed_request = raw_request.split(' ', 2)
        message['method'] = parsed_request[0]
        message['uri'] = parsed_request[1]
        message['version'] = parsed_request[2]
        message['type'] = message_type
        try:
            headers, content_length, body = parse_headers(length, data, parsed_request[0])
            message['headers'] = headers
            if content_length != 0:
                message['Content-Length'] = content_length
            return message, None, body
        except:
            return None, data, None

def print_summary(message,  address):
    print("Connection source: " + address)
    print("HTTP method: " + message['method'])
    print("Destination: " + message['uri'])
    print("Headers: ")
    print(message['headers'])

# returns the host and port
# run by doing:  h, p = parse_uri(dest)
def parse_uri(uri):
    uri_parts = urlparse(uri)
    scheme = uri_parts.scheme
    host = uri_parts.hostname
    # urlparse can't deal with partial URIs that don't include the protocol
    # e.g., push.services.mozilla.com:443
    if host: # correctly parsed
        if uri_parts.port:
            port = uri_parts.port
        else:
            port = socket.getservbyname(scheme)
    else: # incorrectly parsed
        uri_parts = uri.split(':')
        host = uri_parts[0]
        if len(uri) > 1:
            port = int(uri_parts[1])
        else:
            port = 80
    return host, port

def build_message(message, body):
    message_header = '{} {} {}\r\n'.format(message['method'], message['uri'], 'HTTP/1.0') # rebuild message header
    data = ''
    for header in message['headers']:
        data = data + '{}\r\n'.format(header + ': ' + message['headers'][header]) # Format each header properly
    data = data + '\r\n' # add a terminating CRLF
    message_header = message_header.encode('iso-8859-1') # Encode header as bytes
    data = data + body.decode('iso-8859-1') # add body to message
    return message_header + '\r\n'.encode('iso-8859-1') + data.encode('iso-8859-1')

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument('-p', '--port', type=int, help='TCP port for HTTP proxy', default=9999) # register argument

    args = parser.parse_args() # parse the command line

    HOST_ADDRESS = '127.0.0.1' # Set host
    PORT_NUMBER = args.port # Set port

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
                    parsed_message, remainder, body = parse_message(buffer, MessageType.REQUEST)
                    if parsed_message is not None:
                        print_summary(parsed_message, addr[0])
                        host, port = parse_uri(parsed_message['uri'])
                        print('\n')
                        print('Target: {}'.format(host))
                        print('Port: {}\n'.format(port))
                        rebuilt = build_message(parsed_message, body)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                            s2.connect((host, port))
                            s2.sendall(rebuilt)
                            print('Response: {}'.format(s2.recv(5000).decode('iso-8859-1')))
                        break

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()