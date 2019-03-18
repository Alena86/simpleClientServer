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
import config

def main(argv):
	parser = OptionParser()
	parser.add_option('-h', '--host', dest = 'host',
	                    help = 'Server name')
	parser.add_option('-p', '--port', dest = "port",
	                    help = 'Port to connect to')
	parser.add_option('-c', '--config', dest = "config",
	                    help = 'Pass the configuration file where the information of the server is being stored.')


	(options, args) = parser.parse_args()

	if options.host and options.port: 
		host = options.host
		port = options.port
		config = c.Config(host = host, port = port)

	if opriont.config:
		config = c.Config(config = config)

	openConnection(config.host, config.port)

# def openConnection(host, port):
# 	# Create a socket on the server with the internet address and using TCP protocol to transfer data.
	
# 	# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:			# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM), s.close() 
# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	s.bind((host, port))			# Connect socket to particular host and port.
# 	print "Running server on: {}, with the port {}".format(host, port)
# 	s.listen(10)					# Allow connection queue to be no more then 10 requests.
# 	sock, addr = s.accept()			# Waits for incoming connection and receives a new socket from client as well as clients address.
# 	with sock:								#
# 	    print('Connected by', addr)
# 	    while True:							# As long as that client is connected we are listening only to it's requests.
# 	        data = sock.recv(1024)			# Reads whatever client sends and echoes back to the client the result.
# 	        if not data:					# If there is no data, connection has been terminated.
# 	            print "Connection has been terminated"
# 	            break
# 	        sock.sendall(data)
# 	s.close()
def openConnection(host, port):
	if PYTHON_VER == 3:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((host, port))
			s.listen()
			conn, addr = s.accept()
			with conn:
			    print('Connected by', addr)
			    while True:
			        data = conn.recv(1024)
			        if not data:
			            break
			        conn.sendall(data)
	else:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(10)
		conn, addr = s.accept()
		with conn:
		    print('Connected by', addr)
		    while True:
		        data = conn.recv(1024)
		        if not data:
		            break
		        conn.sendall(data)
		s.close()