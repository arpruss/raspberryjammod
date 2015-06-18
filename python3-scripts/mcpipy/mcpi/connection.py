import socket
import select
import sys
import atexit
import os
from .util import flatten_parameters_to_string

""" @author: Aron Nieminen, Mojang AB"""

class RequestError(Exception):
    pass

class Connection:
    """Connection to a Minecraft Pi game"""
    RequestFailed = "Fail"

    def __init__(self, address=None, port=None):
        if address==None:
            try:
                 address = os.environ['MINECRAFT_API_HOST']
            except KeyError:
                 address = "localhost"
        if port==None:
            try:
                 port = int(os.environ['MINECRAFT_API_PORT'])
            except KeyError:
                 port = 4711
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((address, port))
        self.readFile = self.socket.makefile("r")
        self.lastSent = ""
        atexit.register(self.close)

    def __del__(self):
        self.close()

    def close(self):
        try:
            self.readFile.close()
        except:
            pass
        try:
            self.socket.close()
        except:
            pass

    def drain(self):
        """Drains the socket of incoming data"""
        while True:
            readable, _, _ = select.select([self.socket], [], [], 0.0)
            if not readable:
                break
            data = self.socket.recv(1500)
            if not data:
                self.socket.close()
                raise ValueError('Socket got closed')
            e =  "Drained Data: <%s>\n"%data.strip()
            e += "Last Message: <%s>\n"%self.lastSent.strip()
            sys.stderr.write(e)

    def send(self, f, *data):
        """Sends data. Note that a trailing newline '\n' is added here"""
        s = "%s(%s)\n"%(f, flatten_parameters_to_string(data))
        #print "f,data:",f,data
        self.drain()
        self.lastSent = s
        self.socket.sendall(s.encode('utf-8'))

    def send_flat(self, f, data):
        """Sends data. Note that a trailing newline '\n' is added here"""
        #print "f,data:",f,ddata
        s = "%s(%s)\n"%(f, ",".join(data))
        self.drain()
        self.lastSent = s
        self.socket.sendall(s.encode('utf-8'))

    def receive(self):
        """Receives data. Note that the trailing newline '\n' is trimmed"""
        s = self.readFile.readline().rstrip("\n")
        if s == Connection.RequestFailed:
            raise RequestError("%s failed"%self.lastSent.strip())
        return s

    def sendReceive(self, *data):
        """Sends and receive data"""
        self.send(*data)
        return self.receive()

    def sendReceive_flat(self, f, data):
        """Sends and receive data"""
        self.send_flat(f, data)
        return self.receive()
