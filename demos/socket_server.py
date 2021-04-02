import socket

if __name__ == '__main__':

    server = socket.socket()  # 默认是AF_INET、SOCK_STREAM
    server.bind(("0.0.0.0",6868))   # 将主机号与端口绑定到套接字
    server.listen()   # 设置并启动TCP监听器
    while True:
      conn,addr = server.accept()   # 被动接受TCP连接，一直等待连接到达
      while True:
        data = conn.recv(1024)   # 接收TCP消息，并制定最大长度
        if not data:
          print("连接已断开")
          break
        conn.send(data.upper())  # 将接收到的数据转为大写在发回给它
    server.close()