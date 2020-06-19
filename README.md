# Python Network Programming

A project that leverages the Python sockets API to build an HTTP proxy based on the HTTP/1.0 protocol.

A proxy is a network service that receives a connection and reads data from a client, acts on it, and passes that data out to another server. The proxy will also read the server's response, act on it, and send it back to the client. 

The value provided by a proxy is determined by the actions it takes on the data. Here are a few applications of HTTP proxies:

* security (e.g., inspecting HTTP content for malware)
* policy enforcement (e.g., preventing employees from accessing unauthorized content at work)
* software development (e.g., decrypting and examining HTTPS traffic)

To test:
- Open Firefox's general preferences/settings page
- Scroll to the bottom of the page and select Network Settings -> Settings
- Under Configure Proxy Access to the Internet, select Manual proxy configuration
- Set the HTTP Proxy to 127.0.0.1 with Port 9999 (match the port you used to run your proxy)
- Apply your settings and open a new tab to navigate to an HTTP-based site, e.g.,

http://www.washington.edu/ <br>
http://neverssl.com  <br>
http://mit.edu <br>
