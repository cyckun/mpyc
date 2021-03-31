import socket

if __name__ == '__main__':

    client = socket.socket()  # 默认是AF_INET、SOCK_STREAM
    client.connect(("localhost",6868))
    while True:
      s = input(">>")
      client.send(s.encode("utf-8"))
      data = client.recv(1024)
      print("receive from server:", data)
    client.close()