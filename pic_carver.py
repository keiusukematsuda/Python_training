# -*- coding: UTF-8 -*-

import re
import zlib
import cv2

from scapy.all import *

pictures_directory = "pictures"
faces_directory = "faces"
pcap_file = "bhp.pcap"

def get_http_header(http_payload):
    try:
        # HTTPヘッダーを抽出
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]
        
        # ヘッダーの各要素を辞書化
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",headers_raw))

    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers


def extract_image(headers,http_payload):
    image       = None
    image_type  = None

    try:
        if "image" in headers['Content-Type']:
            
            # 画像種別と画像本体の取得
            image_type = headers['Content-Type'].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n")+4:]

            # 画像が圧縮されている場合は解凍
            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif header['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)

            except:
                return None,None

            return image,image_type


def http_assembler(pcap_file):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        
        for packet in session[session]:
            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                    # ストリームの再構築
                    http_payload += src(packet[TCP].payload) 

            except:
                pass

        headers = get_http_header(http_payload)
        
        if headers is None:
            continue

        image,image_type = extract_image(headers,http_payload)

        if image is not None and image_type is not None:
        
            # 画像の保存
            file_name = "%s-pic_carver_%d.%s" % (pcap_file,carved_image,image_type) 

            fd = open("%s/%s" % (pictures_directory,file_name),"wb") 

            fd.write(image)
            fd.close()

            carved_images += 1

            # 顔検出
            try:
                result = face_detect("%s/%s" % (pictures_directory,file_name),file_name)    

                if result is True:
                    faces_detected += 1

            except:
                pass

    return carved_images, faces_detected

carved_images, faces_detected = http_assembler(pcap_file)

print "Extracted: %d images" % carved_images
print "Detected: %d faces" % faces_detected       
