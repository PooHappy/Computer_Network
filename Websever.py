# Import socket module
from socket import * 
import sys # In order to terminate the program
import threading
from threading import Thread
from multiprocessing import Process, Queue

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 8088
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

pandan = 0
subnetwork = []
file = open("subnetworklist.txt", 'r')
for source in file :
    source = source.strip('\n').split('.')
    for i in range(len(source)) :
        source[i] = int(source[i])
    subnetwork.append(source)
file.close()

print('승인된 서브네트워크 목록 :')
print(subnetwork)

while True:
    print('The server is ready to receive')
    connectionSocket, addr = serverSocket.accept()
    print('발신된 IP주소 : %s' %addr[0])
    ip = addr[0].split('.')
    ip_subnetwork = []
    ip_host = []
    i = 0
    while True :
        if i == 3 :
            ip_host.append(int(ip[i]))
            break
        else:
            ip_subnetwork.append(int(ip[i]))
        i += 1
        
    print('발신된 IP주소의 서브네트워크 :', ip_subnetwork)
    print('발신된 IP주소의 호스트 :', ip_host)
    j = 0 
    while j != len(subnetwork) :
        if subnetwork[j] == ip_subnetwork :
            pandan = 1
            break
        else :
            j += 1
            
    if not pandan :
        print('허가되지 않은 IP주소. 입장 불가.')
        break
    
    try:

        message = connectionSocket.recv(2048).decode()
        print(message)

        filename = message.split()[1]
        print(filename)

        myfile = open(filename[1:],'rb')

        response = myfile.read()
        myfile.close()
                  
        header = 'HTTP/1.1 200 OK\n'

        if(filename.endswith(".jpg")):
            filetype = 'image/jpg'
        elif(filename.endswith(".gif")):
            filetype = 'image/gif'
        elif(filename.endswith(".wmv")):
            filetype = 'video/wmv'
        elif(filename.endswith(".mp4")):
            filetype = 'video/mp4'
        elif(filename.endswith(".html")):
            filetype = 'text/html'

        header += 'Content-Type: '+ str(filetype)+'\n\n'
        print(header)

        connectionSocket.send(header.encode())
        connectionSocket.send(response)
        connectionSocket.close()
        sys.exit()

    except IOError:
        header = 'HTTP/1.1 404 Not Found\n\n'
        response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode() 

        print(header)
        connectionSocket.send(header.encode())
        connectionSocket.send(response)
        connectionSocket.close()
        sys.exit()
                
serverSocket.close()
sys.exit()     
