import threading
import ujson
import time

class EventProxy(object):

  def __init__(self, session):
    self.queue = []
    self.EVENT_SEPARATOR = ''
    self.session = session
    self.disconnection = 0
    self.reconnection = 0

  def data_available(self):
    if self.queue:
      return True
    return False

  def update(self, data):
    # Gather result
    timestamp = data['timestamp']
    result = {"result": data}
    # Build SSE message
    eventname = 'periodiclabdata'
    eventid = round(timestamp * 1000)
    eventdata = ujson.dumps(result)
    toSend = 'event: %s\nid: %s\ndata: %s\n\n' % (eventname, eventid, eventdata)
    self.queue.append(toSend)

  def consume(self):
    if self.queue:
      self.queue.pop(0)

  def next(self):
    if self.queue:
      return self.queue[0]
    return None

  def flush(self):
    events = self.EVENT_SEPARATOR.join(self.queue)
    self.queue = []
    return events


class EventGenerator(object):

  def __init__(self, proxy):
    self.proxy = proxy

  def start(self):
    self.running = True
    yield self.proxy.flush()
    while self.running:
      try:
        time.sleep(0.05)
        yield self.proxy.next()
        self.proxy.consume()
      except Exception as e:
        self.running = False