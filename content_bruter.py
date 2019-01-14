# -*- coding:UTF-8 -*-

import urllib2
import threading
import Queue
import urllib

threads         = 50
target_url      = "http://testphp.vulnweb.com"
wordlist_file   = "/tmp/all.txt"
resume          = None
user_agent      = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecko/201000101Firefox/19.0"

def build_wordlist(wordlist_file):
    
    # 単語の辞書を読み取る
    fd = open(wordlist_file, "rb")
    raw_words = fd.readlines()
    fd.close()

    found_resume    = False
    words           = Queue.Queue()

    for word in raw_words:
        
        word = word.rstrip()
    
        if resume is not None:
        
            if found_resume:
                words.put(word)
            else:
                if word == resume:
                    found_resume = True
                    print "Resuming wordlist from: %s" & resume

        else:
            words.put(word)

    return words


def dir_bruter(word_queue, extensions=None):
    
    while not word_queue.empty():
        attempt = word_queue.get()

        attempt_list = []

        # ファイル拡張子があるかどうかチェックする。もしなければディレクトリの
        # パスとして総当たり攻撃の対象とする
        
        if "." not in attempt:
            attempt_list.append("/%s/" % attempt)

        else:
            attempt_list.append("/%s" % attempt)

        # 拡張子の総当たりをしたい場合
        if extensions: 
