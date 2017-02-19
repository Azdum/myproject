import socket

sock_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM,0)
sock_obj.connect(('httpbin.org',80))
sock_obj.send("""POST /post HTTP/1.1
Host: httpbin.org
Content-Type: application/json
Content-Length: 80
Accept: */*

{
    "github": "Azdum",
    "Name": "Roman",
    "Surname": "Kazakov"
}
""".encode())

resp = sock_obj.recv(1024)
print(resp.decode())

sock_obj.close()