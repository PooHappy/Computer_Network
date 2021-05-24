from socket import *
import time

serverName = '192.168.219.109'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

times = 1
error = 0
te = 0
while times <= 1000:
    try : 
        message = "ping[" + str(times) + "]"
        rtt_start = time.time()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        rtt_end = time.time() - rtt_start
    except timeout:
        print('시간 초과')
        error += 1
    except IOError :
        print('정보 손상')
        error += 1
    print(modifiedMessage.decode() + "  " + str(times) + "  RTT: " + str(rtt_end) + " sec")
    times += 1
    te += rtt_end
clientSocket.close()
print('\n')
print(serverName + "에 대한 Ping 통계 : ");
print("횟수 : " + str(times - 1) + ", 손실 : " + str(error) + "  비율 : " + str(error / times) + "%")
print("소요 시간 : " + str(te))
