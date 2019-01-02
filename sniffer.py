# -*- coding: UTf-8 -*-

import socket
import os
import struct
from ctypes import *

# リッスンするホストのIPアドレス
host = "10.0.0.143"

class IP(Structure):
    """IPヘッダーのクラス

    """
    _fields_ = [
        ("ihl",             c_uint8,    4),
        ("version",         c_uint8,    4),
        ("tos",             c_uint8),
        ("len",             c_uint16),
        ("id",              c_uint16),
        ("offset",          c_uint16),
        ("ttl",             c_uint8),
        ("protocol_num",    c_uint8),
        ("sum",             c_uint16),
        ("src",             c_uint32),
        ("dst",             c_uint32)
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        # プロトコルの定数値を名称にマッピング
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"} 

        # 可読なIPアドレス値に変換
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        # 可読なプロトコル名称に変更
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)


class ICMP(Structure):
    """ICMPヘッダーのクラス

    """
    _fields_ = [
        ("type",        c_uint8),
        ("code",        c_uint8),
        ("checksum",    c_uint16),
        ("unused",      c_uint16),
        ("next_hop_mtu",c_uint16)
        ]

    def __new__(self, socket_buffer):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer):
        pass


# rawソケットを作成して、インターフェースにバインド
socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)

sniffer.bind((host, 0))

# キャプチャー結果にIPヘッダーを含めるように指定
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

try:
    while True:
        
        # パケットの読み込み
        raw_buffer = sniffer.recvfrom(65565)[0]
        
        # バッファの最初の20バイトからIP構造体を作成
        ip_header = IP(raw_buffer[0:20])

        # 検出されたプロトコルとホストを出力
        print "Protocol: %s %s -> %s" % (ip_header.protocol, ip_header.src_address, ip_header.dst_address)
    
        # ICMPであればそれを処理
        if ip_header.protocol == "ICMP":
            
            # ICMPパケットの位置を計算
            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]

            # ICMP構造体を作成
            icmp_header = ICMP(buf)

            print "ICMP -> Type: %d Code: %d" % (icmp_header.type, icmp_header.code)

    # Ctrl-Cを処理
except KeyboardInterrupt:
    print "process was over"
