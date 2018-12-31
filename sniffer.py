# -*- coding: UTf-8 -*-

import socket
import os

host = "10.0.0.143"

# rawソケットを作成して、インターフェースにバインド
socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# キャプチャー結果にIPヘッダーを含めるように指定
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# パケットの読み込み
print sniffer.recvfrom(65565)
