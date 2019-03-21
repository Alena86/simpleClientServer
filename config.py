import re
import os

import simplejson

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

HOST = os.uname()[1]
PORT = 8444


class FileNotFound(Exception):
    def __init__(self, message):
        '''
        Exception used in case the specified file doesn't exist.
        :param str message: Message to show when the exception is being raised.
        '''
        self.message = message


class Config(object):
    def __init__(self, host=None, port=None, config=None):
        '''
        Configuration object that holds the connection server name and the post to which to connect to.

        :param str host: name of the server host
        :param int port: number of the port which to listen for instructions
        :param str config: full path of a configuration file with server and port information.
        '''

        self._host = host
        self._port = port
        self._configPath = None

        if config:
            self._configPath = config
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

    @property
    def configPath(self):
        return self._configPath

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
            self._port = int(port)
        except:
            raise Exception.TypeException()

    ########################################################################################################################
    #
    #														Functions
    #
    ########################################################################################################################

    def __getConfigFile(self):
        '''Gets the default configuration file that is specified in this module.'''
        if os.path.exists(CONFIG_PATH):
            if os.path.isfile(CONFIG_PATH):
                self._configPath = CONFIG_PATH
            else:
                raise FileNotFound("Path to configuration file is not a file.")
        else:
            raise FileNotFound("Configuration file doesn't exist.")

    ########################################################################################################################
    #
    #															I/O
    #
    ########################################################################################################################

    def load(self):
        '''
        Loads the configuration file into the Config object for easier access.
        In case there is no config file specified, it reads the default location specified at the top of this module.
        '''
        if self._configPath is None:
            self._configPath = self.__getConfigFile()
        fh = open(self._configPath, 'r')
        data = simplejson.load(fh)
        if "host" in data:
            self.host = data["host"]
        if "port" in data:
            self.port = data["port"]
        fh.close()

    def write(self):
        '''
        Writes json configuration file with host and port settings.
        In case there is no configuration file specified, it writes it to the default location specified at the top of this module.
        '''
        if self._configPath is None:
            self._configPath = self.__getConfigFile()
        fh = open(self.configPath, 'w')
        data = {"host": self.host, "port": self.port}
        simplejson.dump(data, fh, indent=4)
        fh.close()


if __name__ == "__main__":
    configFile = os.path.join(os.path.dirname(__file__), "config_new.json")
    c = Config(config=configFile)
    print "Connecting to:"
    print "Host: ", c.host
    print "Port: ", c.port
