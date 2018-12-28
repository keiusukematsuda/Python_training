# -*- coding: UTF-8 -*-

import socket

target_host = "www.google.com"
target_port = 80

#ソケットオブジェクトの作成
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#サーバへの接続
client.connect((target_host, target_port))

#サーバへのデータの送信
client.send("GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#サーバからのデータの受信
response = client.recv(4096)

print response
