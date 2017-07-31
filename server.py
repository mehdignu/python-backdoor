#!/usr/bin/python2.7
import socket,os
import sys

HOST = '0.0.0.0'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

#Start listening on socket
s.listen(10)
print 'Socket now listening'
conn, addr = s.accept()
print 'Connected with ' + addr[0] + ':' + str(addr[1])

#now keep talking with the client
while 1:
    data = conn.recv(1024)
    print 'data : ' + data
    nextcmd = raw_input("[shell]: ")
    conn.send(nextcmd)
