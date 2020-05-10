# Python Network Programming

## Overview
For this sequence of projects, we will leverage the Python sockets API to build an HTTP proxy based on the HTTP/1.0 protocol.

## About Proxies
A proxy is a network service that receives a connection and reads data from a client, acts on it, and passes that data out to another server. The proxy will also read the server's response, act on it, and send it back to the client. This simple pattern appears frequently in networks and distributed systems and quite frequently provide 

The value provided by a proxy is determined by the actions it takes on the data. Here are a few applications of HTTP proxies:

* security (e.g., inspecting HTTP content for malware)
* policy enforcement (e.g., preventing employees from accessing unauthorized content at work)
* software development (e.g., decrypting and examining HTTPS traffic)

For this sequence of assignments, we are building a proxy to log metadata about HTTP requests and responses.

## Resources
* [Real Python: Sockets Programming in Python](https://realpython.com/python-sockets/)
* [How HTTP Works under the Hood](https://drstearns.github.io/tutorials/http/)
* [Hypertext Transfer Protocol -- HTTP/1.0](https://tools.ietf.org/html/rfc1945)
* [Hypertext Transfer Protocol -- HTTP/1.1](https://tools.ietf.org/html/rfc2616)