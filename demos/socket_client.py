from socket import *
from mpyc.runtime import mpc

LOCAL = False

if LOCAL:
    HOST = '127.0.0.1'  # or 'localhost'
else:
    HOST = '192.168.150.138'
PORT = 6868
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

secnum = mpc.SecInt()
if __name__ == '__main__':
    loop = True
    while loop == True:
        #data1 = input('>')
        #data1 = "i'm alice"
        data1 = secnum(2)
        # data = str(data)
        if type(data1) is str and not data1:
            break
        tcpCliSock.send(data1.encode())
        data1 = tcpCliSock.recv(BUFSIZ)
        if not data1:
            break
        print(data1.decode('utf-8'))
        loop = False
    tcpCliSock.close()
