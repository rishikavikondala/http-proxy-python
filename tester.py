#!/usr/bin/env python3

import argparse
import json
import socket

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
        return None, data

def main():
    data = b''
    with open("resources/post_request.http", "rb+") as f:
        data = f.read()
    message, remainder, body= parse_message(data)
    # print(message['method'])
    # print(message['uri'])
    # print(message['version'])
    # print(message['headers'])
    # print(body)
    for header in message['headers']:
        print(header + ': ' + message['headers'][header])

if __name__=="__main__":
    main()