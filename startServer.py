#!/usr/bin/env python

import sys, os, re
import socket
import logging
import config as c                  # Module that deals with th configuration file.
from argparse import ArgumentParser
from datetime import datetime       # Module to get the date for log creation.

today = datetime.now().strftime("%Y%m%d")
# Specify a location where all the logs are going... This can be defined with the environment variable.
LOG_PATH = os.path.join(os.path.dirname(__file__), "logs")
LOG_NAME = "log_{}.txt".format(today)

# Make sure that the folder for logs exists, if it doesn"t create one.
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

# Default location of the configuration file that holds the default values for running the server.
DEFAULT_CONFIG = os.path.join(os.path.dirname(__file__), 'serverConfig.json')


def main(argv):
    # Parsing the arguments passed to the command.
    parser = ArgumentParser(prog = "startServer", usage = "%(prog)s [args]",
                            description = "Start the server on the machine")

    # Parser for passing the configuration file with server info.
    parser.add_argument("-c", "--configFile",
                        help = "Pass the full path to the configuration file that holds the information about server name and port.")

    # Parser for passing the server information
    parser.add_argument("-s", "--server", type = str, dest = "host", action = "store",
                        help = "Server name/IP address.")
    parser.add_argument("-p", "--port", type = int, dest = "port", action = "store",
                        help = "Port to which to connect to.")

    args = parser.parse_args()

    if args.configFile or args.host or args.port:
        # Check if correct args are passed. Either configuration file or server and port information.
        if getattr(args, "configFile", None):
            if os.path.exists(args.configFile):
                config = c.Config(config = args.configFile)
            else:
                print "!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!! Specified configuration file doesn't exist. Make sure you pass a full path."
                return
        elif getattr(args, 'host', None) and getattr(args, 'port', None):
            config = c.Config(host=args.host, port=args.port)
        else:
            print "!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!! Make sure both server name/IP and port are specified."
            return
    # if there is no arguments passed read the default values from the default configuration file.
    else:
        if os.path.exists(DEFAULT_CONFIG):
            config = c.Config(config=DEFAULT_CONFIG)
        else:
            print "!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!! There is no default configuration file."
            parser.print_help()
            return
    if config:
        # Start listening process on the specified host with the specified port.
        print "Running server on host {} with port {}.".format(config.host, config.port)
        openConnection(config.host, config.port)


def openConnection(host, port):
    logging.basicConfig(filename = os.path.join(LOG_PATH, LOG_NAME), level = logging.DEBUG)
    log("Opened listening port {} on a server {}.".format(port, host), info = True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    while True:
        conn, addr = s.accept()

        log("Established connection from: {} on a port {}.".format(addr[0], addr[1]), info = True)

        # Receive the data in small chunks and retransmit it
        data = conn.recv(1024)
        log("Received '{}'".format(data), info=True)

        # Validate the data that is being passed.
        valid, retValue = validateData(data)

        if valid:
            conn.sendall(retValue)
        else:
            conn.sendall("ERROR: {}".format(retValue))

        log("Closing the connection from: {} on a port {}.".format(addr[0], addr[1]), info=True)
        conn.close()


def replaceInt2Float(matchObj):
    '''
    Checks if found values are integer or float formated, and makes sure that all the numbers are floats.
    :param matchObj: matchObj from the regex
    :return: string of a number formated as float (with .00) in case it doesn't already have decimal formating.
    '''
    if "." in matchObj.group(0):
        return matchObj.group(0)
    else:
        return matchObj.group(0) + ".00"


def validateData(data):
    '''
    Function that validates the data sent from the server. Makes sure that all the numbers are converted to float
    formating in a string and that it can be executed with python eval command.
    :return: tupple -   1st value is boolean if data is valid mathematical equation
                        2nd value is the actual result of the validation.
    '''
    log("Validating {}".format(data), info = True)
    if data:
        # Check that data includes only mathematically valid characters by using regex expression
        # Exclude all the chracters that are not used in the math (eg. letters, {}\!@#$&)
        regexI = r"(?![\+\-\*\/\%\.\(\)\d+])."
        unknown = re.findall(regexI, data)
        if unknown:
            msg = "Found invalid character(s)."
            log(msg, info=True)
            return False, msg
        try:
            # Find all the float/int numbers in the string.
            regex = "\d+\.\d+|\d+"

            # convert all int values to float formated string
            newData = re.sub(regex, replaceInt2Float, data)

            # evaluate the mathematical expression
            res = eval(newData)

            msg = "Result: {}".format(res)
            log(msg, info=True)
            return True, msg
        except:
            msg = "Not a valid mathematical expression.".format(data)
            log(msg, error=True)
            return False, msg
    else:
        msg = "There is no data passed."
        log(msg, warning=True)
        return False, msg

def log(msg, info=False, warning=False, error=False):
    '''
    Function that formats the log to have a date and time in front of every command.
    :param msg: msg to show
    :param info: log the messageas an info message
    :param warning: log the message as a warning message
    :param error: log the message as an error message.
    '''
    curTime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")

    if info:
        logging.info("[{}] {}".format(curTime, msg))
    if warning:
        logging.warning("[{}] {}".format(curTime, msg))
    if error:
        logging.error("[{}] {}".format(curTime, msg))

if __name__ == "__main__":
    main(sys.argv)
