#!/usr/bin/env python

# Import modules for system commands.
import sys, os
import config as c
import socket
from argparse import ArgumentParser
# Import UI modules
# Not sure which tkinter version is installed on the machine
try:
    from Tkinter import *
except:
    from tkinter import *

def main(argv):
    # Parsing the arguments passed to the command.
    parser = ArgumentParser(prog = "client", usage = "%(prog)s [args]",
                            description = "App with a simple UI to send simple mathematical equation to the server.")

    # Parser for passing the configuration file with connection info.
    parser.add_argument("-c", "--configFile",
                        help = "Pass the full path to the configuration file that holds the information about server name and port.")

    # Parser for passing the server information
    parser.add_argument("-s", "--server", type = str, dest = "host", action = "store",
                          help = "Server name/IP address.")
    parser.add_argument("-p", "--port", type = int, dest = "port", action = "store",
                          help = "Port to which to connect to.")

    args = parser.parse_args()

    # Check if correct args are passed. Either configuration file or server and port information.
    if getattr(args, "configFile", None):
        if getattr(args, "configFile", None):
            if os.path.exists(args.configFile):
                config = c.Config(config = args.configFile)
            else:
                print "!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!! Specified configuration file doesn't exist. Make sure you pass a full path."
                return
    elif args.host and args.port:
        config = c.Config(host = args.host, port = args.port)
    elif (args.host or args.port):
        print "!!!!!!!!!!!!!!!!!!!!!!!ERROR!!!!!!!!!!!!!!!!!!!!!!!!!! Make sure to specify both host and port."
        return
    else:
        parser.print_help()
        return

    # If correct data is passed, configuration object has been created and UI is getting created.
    if config:
        # Create UI
        dlg(config)


class dlg(object):
    def __init__(self, cObj):
        '''
        Simple UI for server/client communication.
        :param cObj: configuration object with server host/port information
        '''
        self.win = Tk()
        self.win.geometry('720x560')

        self.__cObj = cObj

        self.lbl_info = Label(self.win, text = "Input Expression:")
        self.lbl_info.pack()
        self.ent = Entry(self.win)
        self.ent.grid(column = 0, row = 0)
        self.ent.bind("<Return>", self.evaluate)
        self.ent.focus()
        self.ent.pack()

        self.btn_exec = Button(self.win, text = "Execute on server", bg = "green", fg = "black", command = self.evaluate)
        self.btn_exec.grid(column=0, row=2)
        self.btn_exec.pack()

        self.lbl_res = Label(self.win, text = "Output: ", )
        self.lbl_res.pack()
        # self.lbl_res.grid(column = 0, row = 3)

        self.output = Text(self.win, height = 100, width = 100)
        self.output.pack()

        self.win.mainloop()

    @property
    def cObj(self):
        '''
        :return: configuration object that holds server host/port information
        '''
        return self.__cObj

    def evaluate(self, sender = None):
        '''
        Method that open connection to the server and sends the request to it.
        :param sender: object that called this method. Most likely Entry from the UI.
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print "Sending data to the host {} on a port {}.".format(self.cObj.host, self.cObj.port)
        try:
            # Create connection with the server
            s.connect((self.cObj.host, self.cObj.port))

            try:
                # Get the inputed text in the Entry and send it to the server for validation.
                input = self.ent.get()
                if input:
                    s.sendall(input)

                    data = s.recv(1024)
                    self.output.insert(END, "{}\n".format(data))
                else:
                    self.output.insert(END, "Missing expression. Need to supply the expression to validate.\n")
            finally:
                s.close()
        except:
            self.output.insert(END, "Connection refused, invalid host or port.\n \tHOST: {}, PORT {}.\n".format(self.cObj.host, self.cObj.port))

if __name__ == "__main__":
    main(sys.argv))