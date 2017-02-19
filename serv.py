import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 8000))
s.listen(1)

while 1:
    conn, addr = s.accept()
    data = conn.recv(2048)
    res = data.split(' ')
    f = open(res[1], 'rb')
    conn.send("HTTP/1.1 200 OK \n\n\n" + f.read())
conn.close()