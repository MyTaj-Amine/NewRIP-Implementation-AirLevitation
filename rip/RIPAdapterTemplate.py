'''
@author: jcsombria
'''
import random
from rip.RIPGeneric import RIPGeneric

class RIPAdapterTemplate(RIPGeneric):
  '''
  RIP Adapter Template
  '''

  def __init__(self, info={}):
    '''
    Constructor
    '''
    super().__init__(info)

  def default_info(self):
    '''
    You can provide default metadata here. AppConfig will override this definition.
    '''
    return {
      'name':'RIPAdapterTemplate',
      'description':'A template to extend RIP Generic',
      'authors':'J. Chacon',
      'keywords':'Adapter Template',
      'readables':[{
        'name':'time',
        'description':'Server time in seconds',
        'type':'float',
        'min':'0',
        'max':'Inf',
        'precision':'0',
      }, {
        'name':'random',
        'description':'Random value generator',
        'type':'float',
        'min':'0',
        'max':'1',
        'precision':'0'
      }],
      'writables': [{
        'name':'seed',
        'description':'Random seed',
        'type':'float',
        'min':'0',
        'max':'1',
        'precision':'0'
      }],
    }

  def set(self, expid, variables, values):
    '''
    Write on or more variables
    '''
    n = len(variables)
    for i in range(n):
      try:
        n, v = variables[i], values[i]
        if v in writables:
          self.n = v
      except:
        pass

  def get(self, expid, variables):
    '''
    Retrieve one or more variables under request
    '''
    toReturn = {}
    n = len(variables)
    for i in range(n):
      name = variables[i]
      try:
        toReturn[name] = random.rand
      except:
        pass
    return toReturn

  def getValuesToNotify(self):
    '''
    Variables to include in periodic SSE updates
    '''
    return [
      ['time', 'random'],
      [self.sampler.lastTime(), self.random]
    ]

  @property
  def seed(self):
    return self._seed

  @seed.setter
  def seed(self, value):
    random.seed(value)

  @property
  def random(self):
    return random.random()

  @random.setter
  def random(self, value):
    pass
