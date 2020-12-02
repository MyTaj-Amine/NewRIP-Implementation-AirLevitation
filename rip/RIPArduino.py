'''
@author: jcsombria
'''
import ujson
import serial
import serial.threaded
from serial import threaded, SerialException
from serial.tools import list_ports
import signal
import threading

from rip.RIPGeneric import RIPGeneric

default_info = {
  'name': 'Arduino',
  'description': 'An implementation of RIP to control Arduino',
  'authors': 'J. Chacon',
  'keywords': 'Arduino, RIP',
}

class RIPArduino(RIPGeneric):
  '''
  RIP Arduino Adapter
  '''

  def __init__(self, info=default_info):
    '''
    Constructor
    '''
    super().__init__(info)
    self.arduino = None
    self.arduino_connected = False
    self.measurement = {}

  def connect_arduino(self):
    ports = list_ports.comports()
    self.arduino_connected = True
    for p in ports:
      try:
        print('[INFO] Connecting to %s' % p.device)
        self.arduino = serial.serial_for_url(p.device, baudrate=115200, timeout=5, write_timeout=5)
        self.arduino_thread = threading.Thread(target=self.update).start()
        break
      except:
        print('[INFO] Cannot connect to %s, trying another port' % p.device)
    if self.arduino is None or not self.arduino.is_open:
      print('[ERROR] Cannot connect to arduino, stopping server')
      self.stop()

  def start(self):
    super().start()
    print("I'm sur i'm calling start")
    if not self.arduino_connected:
      self.connect_arduino()

  def stop(self):
    super().stop()
    self.arduino_connected = False
    if self.arduino is not None:
      self.arduino.close()
      self.arduino = None
    self.measurement = {}

  def update(self):
    while self.arduino_connected:
      try:
        data = self.arduino.read_until()
        print(data)
        self.measurement = ujson.loads(data)
      except (ValueError, TypeError) as e:
        print('[WARNING] Ignoring invalid data from Arduino')
      except SerialException as e:
        print('[WARNING] Disconnected from Arduino.')
        self.stop()
    print('[INFO] Stopping arduino thread')

  def set(self, expid, variables, values):
    '''
    Writes one or more variables to the Arduino
    '''
    toWrite = {}
    n = len(variables)
    for i in range(n):
      try:
        toWrite[variables[i]] = values[i]
      except:
        pass
    toArduino = ujson.dumps(toWrite) + "\n"
    if self.arduino_connected:
      self.arduino.write(toArduino.encode('utf-8'))

  def get(self, expid, variables):
    '''
    Retrieve one or more variables from the workspace of the current Octave session
    '''
    toReturn = {}
    n = len(variables)
    for i in range(n):
      name = variables[i]
      try:
        toReturn[name] = self.measurement[name]
      except:
        pass
    return toReturn

  def getValuesToNotify(self):
    try:
      toReturn = [[
        'time',
        'timestamp',
        'y'
      ], [
        self.sampler.lastTime(),
        self.measurement['timestamp'],
        self.measurement['y']
      ]]
    except:
      toReturn = [
        ['time'],
        [self.sampler.lastTime()]
      ]
    return toReturn
