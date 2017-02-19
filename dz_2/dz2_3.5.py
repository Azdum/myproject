import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('httpbin.org', 80))
s.send("GET /cookies HTTP/1.1\nHost: httpbin.org\nAccept: */*\n\n".encode()) 
print(s.recv(2048).decode())
s.close()