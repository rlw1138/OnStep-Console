# Interface to a serial device

import time
import sys
import serial
from .platform import clearscreen

class tty:

  #def __init__(self, port = '/dev/ttyUSB0', baud=9600): # linux
  def __init__(self, port = 'COM8', baud=9600):
    try:
      self.ser = serial.Serial(port, baud)
    except serial.SerialException as e:
      clearscreen() # wipe screen so we can read the message
      sys.stderr.write('ERROR: Could not open port: ' + port + '\n')
      sys.exit(1)

  def open(self):
    self.ser.isOpen()

  def send(self, string):
    b = string.encode('utf-8')
    self.ser.write(b)
    time.sleep(0.05)

  def recv(self):
    output = ''
    while self.ser.inWaiting() > 0:
      output += self.ser.read(1).decode('utf-8')
    return output

  def close(self):
    self.ser.close()
