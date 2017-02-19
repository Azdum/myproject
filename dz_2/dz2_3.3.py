import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('httpbin.org', 80))
s.send("POST /post HTTP/1.1\nHost: httpbin.org\nAccept: */*\nContent-Length: 35\nContent-Type: application/x-www-form-urlencoded\n\n\nfoo=bar&1=2&2%2F0=&error=True\nConnection: close\n\n".encode()) 
print(s.recv(2048).decode())
s.close()