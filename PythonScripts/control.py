'''
Scripts for communication between computer and arduino

Created by: Tomas Hromada
  tomashromada1@gmail.com
Github: https://github.com/tomash1234/

See: https://www.youtube.com/watch?v=S3CwzkT6cK4
'''

import socket
import requests

from PIL import Image
from io import BytesIO

import time
import shutil

UDP_IP = "192.168.1.108" # IP adress of arduino
UDP_PORT = 8525
KEY = 44

sock = socket.socket(socket.AF_INET,
                  socket.SOCK_DGRAM)


def pitch(angle):
    a = KEY%256
    b = 88%256
    s = angle%256
    
    buf = [a, b, s]
    data = bytes(buf)
    sock.sendto(data, (UDP_IP, UDP_PORT))

def rotate(angle):
    a = KEY%256
    b = 120%256
    s = angle%256
    
    buf = [a, b, s]
    data = bytes(buf)
    sock.sendto(data, (UDP_IP, UDP_PORT))

def shot(shot):
    a = KEY%256
    b = KEY%256
    if shot:
        s = 64%256
    else:
        s = 0%256
    
    buf = [a, b, s]
    data = bytes(buf)
    sock.sendto(data, (UDP_IP, UDP_PORT))

def shotandreloade():
    shot(False)
    time.sleep(0.8)
    shot(True)
    time.sleep(1)
    shot(False)

def laser(on):
    a = KEY%256
    b = 140%256
    if on:
        s = 100%256
    else:
        s = 0%256
    
    buf = [a, b, s]
    data = bytes(buf)
    sock.sendto(data, (UDP_IP, UDP_PORT))
