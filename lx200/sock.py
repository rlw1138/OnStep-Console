import socket
import os
import sys
import logging
import time

MAX_LEN = 32
RETRY_ATTEMPTS=10
RETRY_INTERVAL=2

logging.info('Importing "sock.py" and establishing connection')

class sock:
    def __init__(self, sock=None):
        self.sock = None
        self.host = ''
        self.port = ''

    def connect(self, host = '', port = '', retry=0):
        self.retry=retry
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host != '':   self.host = host
        if port != '':   self.port = port

        for i in range(RETRY_ATTEMPTS):
            try:
                self.sock.connect((self.host, self.port))
            except OSError:
                msg="Exception occurred in sock.connect(HOST={}, PORT={}), retrying ({})".format(self.host, self.port, i+1)
                logging.error(msg, exc_info=True)
                #self.sock.close()
                time.sleep( RETRY_INTERVAL * i )
                continue # retrying
            else:
                break # we're connected
        else: #only after "for i in range(RETRY_ATTEMPTS):" fails
            logging.critical(f"Persistent networking error in sock.connect() -- too many retries")
            logging.info(f"-- exit to system --")
            sys.exit()

    def send(self, msg):
        self.connect(self.host, self.port)
        self.sock.sendall(msg.encode('utf-8'))
        #self.sock.close()

    def recv(self):
        data = self.sock.recv(MAX_LEN)
        #self.sock.close()
        return data.decode('utf-8')

    def recv_raw(self):
        data = self.sock.recv(MAX_LEN)
        #self.sock.close()
        return data
