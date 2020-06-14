'''
This file was made to store old snippets of code that I might need again later.
'''

# One version of test code for the parsing functionality
# data = b''
# with open("resources/get_request.http", "rb+") as f:
#     data = f.read()
# message, remainder = parse_message(data)
# print(message['method'])
# print(message['uri'])
# print(message['version'])
# print(message['headers'])
# print(remainder)

# Another version of test code for the parsing functionality
# data = b'GET http://neverssl.com/ HTTP/1.1\nHost: neverssl.com\nConnection: keep-alive\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8\nAccept-Encoding: gzip, deflate, br\nAccept-Language: en-US,en;q=0.9'
# length, req = get_request(data)
# print(req)
# print(parse_headers(length, data))