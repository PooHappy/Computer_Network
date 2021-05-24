from socket import *
import time
serverName = '192.168.219.109'
serverPort = 12000

times = 1
error = 0
te = 0
while times <= 1000 :
    try :
        start = time.time()
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.settimeout(1)
        clientSocket.connect((serverName,serverPort))
        end = time.time() - start
        sentence = "ping[" + str(times) + "]"

        rtt_start = time.time()
        clientSocket.send(sentence.encode())
        modifiedsentence = clientSocket.recv(1024)
        rtt_end = time.time() - rtt_start
    except timeout :
        print('시간 초과')
        error += 1
    except  IOError :
        error += 1
    print('From Server:', modifiedsentence.decode() + "  " + str(times) + "  RTT: " + str(rtt_end) + " sec")
    print("소요 시간 : " + str(end))
    times += 1
    clientSocket.close()
    te += end
    te += rtt_end
print('\n')
print(serverName + "에 대한 Ping 통계 : ");
print("횟수 : " + str(times-1) + ", 손실 : " + str(error) +"  비율 : "+ str(error/times) + "%")
print("소요 시간 : " + str(te))
