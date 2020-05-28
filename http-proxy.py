#!/usr/bin/env python3

# add import statements here
import argparse
import json
import socket
from urllib.parse import urlparse

# define classes, enums, etc here

# get length of buffer using len() function

# TESTING
# Print out the rebuilt message to see if it looks correct

# define functions here
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

def parse_message(data):
    message = {}
    length, raw_request = get_fields(data)
    parsed_request = raw_request.split(' ', 2)
    message['method'] = parsed_request[0]
    message['uri'] = parsed_request[1]
    message['version'] = parsed_request[2]
    try:
        headers, content_length, body = parse_headers(length, data, parsed_request[0])
        message['headers'] = headers
        if content_length != 0:
            message['Content-Length'] = content_length
        # if int(content_length) > 0:
        #     # need to look at the unparsed portion of the buffer for the message body
        # if # unparsed portion of buffer < content-length:
        #     # return to the recv() loop and wait for the remaining data
        # elif # unparsed portion of buffer > content-length:
        #     # extra bytes should remain in the buffer 
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
    # urlparse can't deal with partial URI's that don't include the 
    # protocol, e.g., push.services.mozilla.com:443
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
    # Please note that we are replacing the original version (this is intentional)
    message_header = '{} {} {}\r\n'.format(message['method'], message['uri'], 'HTTP/1.0')
    data = ''
    for header in message['headers']:
        data = data + '{}\r\n'.format(header + ': ' + message['headers'][header]) # Format each header properly
    # Don't forget to add a terminating CRLF
    data = data + '\r\n'
    # Encode the header portion of the message as bytes
    message_header = message_header.encode('iso-8859-1')
    # Do you have a message body? Add it back now
    data = data + body.decode('iso-8859-1')
    return message_header + '\r\n'.encode('iso-8859-1') + data.encode('iso-8859-1')

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
                    parsed_message, remainder, body = parse_message(buffer)
                    if parsed_message is not None:
                        print_summary(parsed_message, addr[0])
                        print('\n')
                        host, port = parse_uri(parsed_message['uri'])
                        print('Target: {}{}\n'.format(host, port))
                        rebuilt = build_message(parsed_message, body)
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
                            s2.connect((host, port))
                            s2.sendall(rebuilt)
                            print('Response: {}'.format(s2.recv(250)))
                        break

# if statement so main() runs by default from command line
if __name__=="__main__":
    main()