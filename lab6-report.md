# Lab 6 Report - Python and Socket Basics

INFO 314 
DATE:
NAME: 

## Overview  

**In the remaining weeks of the quarter, we will create a network service using the Python sockets API. In this lab, we will introduce the basic concepts of network programming with a Sockets API and build a pair of toy applications.**

**Follow the procedures provided to you on Canvas and the course website. When you are finished, answer the following questions and include the completed report in your Pull Request. Be sure to cite any external references that you use.**

## Questions

1. **What two values are returned by the accept() function in the Python socket library?**

The `accept()` function returns the value pair `(conn, address)`. In this pair, `conn` is a new socket object which can be used to send and receive data on the network connection. `address` is the address that is connected to the other end of the connection formed with `conn`. (https://docs.python.org/3/library/socket.html#socket.socket.recv)

2. **Briefly describe the difference between bind(), listen(), and accept()?**

`bind()` associates an existing socket with the address provided in the function parameter. `listen()` gives a server the ability to accept connections. `accept()` matches a new socket with the address of an existing connection. The difference between the three has to do with what they enable, and whether they deal with new or existing entities. (https://docs.python.org/3/library/socket.html#socket.socket.recv)

3. **How can we get a server socket to listen and accept connections on all available IPv4 interfaces and addresses?**

To get a server socket to listen and accept connections on all available IPv4 interfaces and addresses, set the host at the top of the server program with the following syntax: `HOST = ''`. (https://docs.python.org/3/library/socket.html#socket.socket.recv)

4. **How do we create a server socket that restricts communication to processes running on the same host?**

To do this, restrict communication to `localhost`. (https://realpython.com/python-sockets/)

5. **What happens if a client or server calls recv() on a connection, but there isn't any data waiting to be processed?**

If a client or server calls `recv()` on a connection and there isn't any data waiting to be processed, then no more data can ever be received on the connection as it has been closed or is in the middle of being closed.
(https://docs.python.org/2/howto/sockets.html)

6. **How many characters are in the basic ASCII character set? How many bits are required to represent an ASCII character value?** 

There are 128 characters in the basic ASCII character set. One ASCII character value has 8 bits.

7. **How many bytes are used to encode an ASCII value in UTF-8?**

4 bytes are needed to encode an ASCII value in UTF-8.

8. **What is the UTF-8 encoding of your favorite emoji (provide the answer in hex)?**

The UTF-8 encoding for my favorite emoji is F0 9F 99 8F. (https://apps.timwhitlock.info/unicode/inspect/hex/1F64F)

9. **Which character encoding is specified by the RFCs for HTTP/1.0 and HTTP/1.1?**

ISO-8859-1 is the character encoding specified by the RFCs for HTTP. (https://tools.ietf.org/html/rfc5987)

10. **What line ending is used to delimit request and response headers in HTTP/1.0 and HTTP/1.1?**

The line ending used for these headers is a carriage return. (https://docs.citrix.com/en-us/netscaler/12/appexpert/http-callout/http-request-response-notes-format.html)