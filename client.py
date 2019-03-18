import sys

if sys.version_info[0] == 2:
	print("version 2")
	PYTHON_VER = 2
	print ("Running python version {}.{}".format(sys.version_info[0], sys.version_info[1]))
else: 
	print ("version 3")
	PYTHON_VER = 3
	print ("Running python version {sys.version_info[0]}.{sys.version_info[1]}")

import socket

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server
if PYTHON_VER == 3:
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((HOST, PORT))
		s.sendall(b'Hello, world')
		data = s.recv(1024)

	print('Received', repr(data))

else:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall(b'Hello, world')
	data = s.recv(1024)

	print('Received', repr(data))