# Python Network Programming

A project that leverages the Python sockets API to build an HTTP proxy based on the HTTP/1.0 protocol.

A proxy is a network service that receives a connection and reads data from a client, acts on it, and passes that data out to another server. The proxy will also read the server's response, act on it, and send it back to the client. 

The value provided by a proxy is determined by the actions it takes on the data. Here are a few applications of HTTP proxies:

* security (e.g., inspecting HTTP content for malware)
* policy enforcement (e.g., preventing employees from accessing unauthorized content at work)
* software development (e.g., decrypting and examining HTTPS traffic)
