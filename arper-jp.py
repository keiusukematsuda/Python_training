# -*- coding: UTF-8 -*-

from scapy.all import *
import os
import sys
import threading
import signal

interface       =   "eth0"
target_ip       =   "10.0.0.154"
gateway_ip      =   "10.0.0.1"
packet_count    =   1000

# インターフェースの設定
conf.iface = interface

# 出力の停止
conf.verb = 0

print "[*] Setting up %s" % interface

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "[!!!] Failed to get gateway MAC. Exiting."
    sys.exit(0)
else:
    print "[*] Gateway %s is at %s" % (gateway_ip,gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print "[!!!] Failed to get target Mac. Exiting."
    sys.exit(0)
else:
    print "[*] Traget %s is at %s" % (target_ip,target_mac)
