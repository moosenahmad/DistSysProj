import socket

ip = raw_input("Enter server ip: ")
host = ip
port = 8080
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
print("You are connected to the server\n")
data = s.recv(1024).decode('utf-8')
print('Server: ' + data)
while 1:
     data = s.recv(1024).decode('utf-8')
     print('Server: ' + data)
     if(data == "cmdclose"):
        break
     elif(data == "clientfile"):
        s.sendall("ready".encode('utf-8'))
        f = open('clients.txt','wb')
        l = s.recv(1024)
        while(l):
                if(l == "done...transfer"):
                     break
                else:
                     f.write(l)
                     l = s.recv(1024)
        f.close()
	s.sendall("Done receiving".encode('utf-8'))
     else:
	s.sendall("Received".encode('utf-8'))
