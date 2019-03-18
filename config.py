import re
import os

import simplejson

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

HOST = os.uname()[1]
PORT = 1080

class Config(object):
	def __init__(self, host = None, port = None, config = None):
		'''
		Configuration object that holds the information about the connection like a server name and the post to which to connect to. 

		:param str host: name of the server host
		:param int port: number of the port which to listen for instructions
		:param str config: string path to the configuration file to read the information about the server and port.
		'''

		self._host = host
		self._port = port
		if host and port: 
			self.write()

		if config:
			self.__configPath = None
			self.load()

	########################################################################################################################
	#
	#													Setters and getter
	#
	########################################################################################################################

	@property
	def host(self):
		return self._host
	
	@property
	def port(self):
		return self._port

	@host.setter
	def host(self, host): 
		if isinstance(host, str):
			self._host = host
		elif re.search("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", host):
			self._host = host
		else:
			raise Exception.TypeException()

	@port.setter
	def port(self, port):
		try:
			self._port = int(port):
		exception:
			raise Exception.TypeException()

	@property
	def configPath(self):
		return self.__configPath
	
	########################################################################################################################
	#
	#														Functions
	#
	########################################################################################################################

	def _getConfigFile(self):
		if os.path.exists(CONFIG_PATH):
			if os.path.isfile(CONFIG_PATH): 
				self.__configPath = CONFIG_PATH
			else:
				raise Exception.FileNotFoundError("Config file is not a file.")
		else:
			raise Exception.FileNotFoundError("Config file doesn't exist.")


	########################################################################################################################
	#
	#															I/O
	#
	########################################################################################################################

	def load(self): 
		print "load"
		self._getConfigFile()
		fh = open(self.__configPath, 'r')
		data = simplejson.load(fh)
		if "host" in data:
			self._host = data["host"]
		elif "port" in data:
			self._port = data["port"]
		fh.close()
	
	def write(self):
		self._getConfigFile()
		fh = open(self.configPath, 'w')
		data = {"host": self.host, "port": self.port}
		simplejson.dump(data, fh, indent = 4)
		fh.close()



if __name__ == "__main__":
	configFile = os.path.join(os.path.dirname(__file__), "config.json")
	c = Config(config = configFile)
	print "Connecting to:"
	print "Host: ", c.host
	print "Port: ", c.port