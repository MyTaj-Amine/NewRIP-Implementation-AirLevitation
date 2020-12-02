'''
@author: jcsombria
'''
import random
import time
import cherrypy


class Signal(object):
  '''
  A Signal that can be sampled
  '''

  def sample(self):
    '''
    Get the instantaneous value of the signal
    '''
    return 5*random.random()

class Sampler(object):
  '''
  An abstract Sampler
  '''

  def __init__(self, signal):
    self.signal = signal
    self.observers = []
    self.steps = 0

  def register(self, o):
    self.observers.append(o)

  def remove(o):
    try:
      self.observers.remove(o)
    except:
      pass

  def notify(self, data):
    for o in self.observers:
      try:
        o.update(data)
      except:
        pass

  def start(self):
    self.running = True
    while self.running:
      self.steps += 1
      data = self.signal.sample()
      self.notify(data)
      self.wait()

  def stop(self):
    self.running = False

  def wait(self):
    pass

class PeriodicSampler(Sampler):

  def __init__(self, period, signal):
    super().__init__(signal)
    self.Ts = period
    self.reset()

  def notify(self, data):
    data = {
      'timestamp': self.last,
      'value': self.signal.sample(),
    }
    super().notify(data)

  def wait(self):
    # Wait until the next sampling time
    self.next = self.time / self.Ts + self.Ts
    interval = self.Ts - self.time % self.Ts
    time.sleep(interval)
    self.time = time.time() - self.t0
    self.last = self.time

  def sample(self):
    self.signal.sample()

  def reset(self):
    # Reset to the initial state
    self.t0 = time.time()
    self.time = 0
    self.last = 0
    self.next = self.Ts

  def delta(self):
    # Compute the time elapsed since the last sampling time
    return self.time - self.last

  def lastTime(self):
    # Last sampling time
    return self.last


class PeriodicSoD(PeriodicSampler):

  def __init__(self, period, signal, threshold):
    super().__init__(period, signal)
    self.threshold = threshold
    self.firstStep = True

  def condition(self):
    sample = self.signal.sample()
    return abs(sample - self.lastSample) > self.threshold

  def wait(self):
    event = False
    while not event:
      try:
          if self.firstStep:
              event = True
              self.firstStep = False
              self.lastSample = self.signal.sample()
          else:
              event = self.condition()
      except:
        print('Cannot evaluate sampling condition.')
      super().wait()
