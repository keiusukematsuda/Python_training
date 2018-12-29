# -*- coding: UTF-8 -*-

import threading
import paramiko
import subprocess

def ssh_command(ip, user, passwd, command):
    """SSHでコマンドを実行する関数
    
    """

    client = paramiko.SSHClient()
    # パスワード認証の代わりに鍵認証を使用する場合
    # client.load_host_keys('/home/ec2-user/.ssh/known_hosts')
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=user, password=passwd)
    ssh_session = client.get_transport().open_session()
    if ssh_session.active:
        ssh_session.exec_command(command)
        print ssh_session.recv(1024)
    return

ssh_command('10.0.0.136', 'ec2-user', 'ec2-user', 'id')
