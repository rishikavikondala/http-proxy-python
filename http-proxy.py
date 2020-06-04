#!/usr/bin/env python3

import argparse
import json
import socket
import datetime
from urllib.parse import urlparse
from enum import Enum, auto

# Enumeration to represent message types 
class MessageType(Enum):
    REQUEST = auto() # constant values are auto-assigned
    RESPONSE = auto() # constant values are auto-assigned

# Gets fields from first line of request/response
def get_fields(data):
    raw_req = data.partition(b'\n')
    return len(raw_req[0]), raw_req[0].strip().decode('iso-8859-1')

# Parses one line of an http request/response
def parse_line(data, encoding = 'iso-8859-1'):
    fields = data.partition(b'\n')
    if len(fields[1]) == 0:
        return None, data
    line = fields[0].rstrip(b'\r').decode(encoding)
    if len(fields[2]) == 0:
        return line, None
    return line, fields[2]

# Populates http headers into a dictionary
def parse_headers(index, data, method):
    headers = {}
    data = data[index+1:]
    line, unparsed = parse_line(data)
    content_length = None
    body = b''
    while line != '':
        if line is None:
            raise Exception
        else:
            parts = line.split(':', 1)
            headers[parts[0]] = parts[1].strip()
            if parts[0] == 'Content-Length':
                content_length = int(parts[1].strip())
        line, unparsed = parse_line(unparsed)
    if content_length is not None and method != 'GET':
        if len(unparsed) < content_length:
            raise Exception
        body = unparsed[0: content_length]
    return headers, content_length, body

# parses HTTP messages' fields and headers
def parse_message(data, message_type):
    message = {}
    length, raw_request = get_fields(data)
    parsed_request = raw_request.split(' ', 2)
    if message_type is MessageType.REQUEST:
        message['method'] = parsed_request[0]
        message['uri'] = parsed_request[1]
        message['version'] = parsed_request[2]
    elif message_type is MessageType.RESPONSE:
        message['version'] = parsed_request[0]
        message['code'] = parsed_request[1]
        message['status'] = parsed_request[2]
    message['type'] = message_type
    try:
        headers, content_length, body = parse_headers(length, data, parsed_request[0])
        message['headers'] = headers
        if content_length != 0:
            message['Content-Length'] = content_length
        return message, None, body
    except:# Exception as E:
        #print(E)
        return None, data, None

# for testing/development: prints relevant information for a connection
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

# rebuilds a parsed HTTP message
def build_message(message, body):
    if message['type'] is MessageType.REQUEST:
        message_header = '{} {} {}\r\n'.format(message['method'], message['uri'], 'HTTP/1.0') # rebuild message header
    elif message['type'] is MessageType.RESPONSE:
        message_header = '{} {} {}\r\n'.format(message['version'], message['code'], message['status']) # rebuild message header
    data = ''
    for header in message['headers']:
        data = data + '{}\r\n'.format(header + ': ' + message['headers'][header]) # Format each header properly
    data = (data + '\r\n').encode('iso-8859-1') # add a terminating CRLF
    message_header = message_header.encode('iso-8859-1') # Encode header as bytes
    data = data + body # add body to message
    return message_header, message_header + data

# prints out an HTTP access log with commonly used formatting
def access_log(host, dt, req_line, code, content_length, referer, user_agent):
    response = '{} [{}] "{}" {} {} {} {}'.format(host, dt, req_line.decode('iso-8859-1').strip(), code, content_length, referer, user_agent)
    return response 

def main():
    parser = argparse.ArgumentParser() 
    parser.add_argument('-p', '--port', type=int, help='TCP port for HTTP proxy', default=9999) # register argument
    args = parser.parse_args() # parse the command line
    HOST_ADDRESS = '127.0.0.1' # Set host
    PORT_NUMBER = args.port # Set port

    # Accept new connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as request_socket:
        request_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        request_socket.bind((HOST_ADDRESS, PORT_NUMBER))
        request_socket.listen()
        while True:
            conn, addr = request_socket.accept()
            with conn:
                buffer = b''
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    buffer = buffer + data
                    request_message, remainder, body = parse_message(buffer, MessageType.REQUEST)
                    if request_message is not None:
                        break
                host, port = parse_uri(request_message['uri'])
                message_header, rebuilt = build_message(request_message, body)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as response_socket:
                    response_socket.connect((host, port))
                    response_socket.sendall(rebuilt)
                    buffer = b''
                    while True:
                        raw = response_socket.recv(4096)
                        if not raw:
                            break
                        buffer = buffer + raw
                        response_message, remainder, body = parse_message(buffer, MessageType.RESPONSE)
                        if response_message is not None:
                            break
                    dt = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S')
                    length, res_fields = get_fields(buffer)
                    content_length = 0
                    content_length = response_message['Content-Length']
                    referer = '-'
                    if 'Referer' in request_message['headers']:
                        referer = request_message['headers']['Referer']
                    user_agent = '-'
                    if 'User-Agent' in request_message['headers']:
                        user_agent = request_message['headers']['User-Agent'].strip()
                    print(access_log(addr[0], dt, message_header, res_fields.split(' ', 2)[1], content_length, referer, user_agent))
                message_header, rebuilt = build_message(response_message, body)
                conn.sendall(rebuilt)

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()
