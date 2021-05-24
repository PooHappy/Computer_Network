# Import socket module
from socket import *
import sys  # In order to terminate the program
from threading import Thread
import threading

class ClientThread(threading.Thread):
    def __init__(self, ip, port, con, num):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.con = con
        self.num = num

    def run(self):
        try:
            # Receives the request message from the client
            message = self.con.recv(2048).decode()
            print(message)
            print()
            print('%d번째 쓰레드 오픈' %self.num)
            # Extract the path of the requested object from the message
            # The path is the second part of HTTP header, identified by [1]
            filename = message.split()[1]
            print(filename)

            # Because the extracted path of the HTTP request includes
            # a character '\', we read the path from the second character
            myfile = open(filename[1:], 'rb')

            # Store the entire contenet of the requested file in a temporary buffer
            response = myfile.read()
            myfile.close()

            # Send the HTTP response header line to the connection socket
            header = 'HTTP/1.1 200 OK\n'

            if (filename.endswith(".jpg")):
                filetype = 'image/jpg'
            elif (filename.endswith(".gif")):
                filetype = 'image/gif'
            elif (filename.endswith(".mp4")):
                filetype = 'video/mp4'
            elif (filename.endswith(".wmv")):
                filetype = 'video/wmv'
            elif(filename.endswith(".html")):
                    filetype = 'text/html'

            header += 'Content-Type: ' + str(filetype) + '\n\n'
            print(header)

            self.con.send(header.encode())
            self.con.send(response)
            self.con.close()
            print()
            print('%d번째 File Close' %self.num)
            print()
    
        except IOError:
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode()

            print(header)
            self.con.send(header.encode())
            self.con.send(response)
            self.con.close()

