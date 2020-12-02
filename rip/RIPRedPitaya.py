'''
@author: Amine
'''
from rip.RIPGeneric import RIPGeneric

class RIPRedPitaya(RIPGeneric):
  '''
  RIP Implementation for Red Pitaya
  '''

  def __init__(self, info):
    '''
    Constructor
    '''
    super().__init__(info)


  def default_info(self):
    '''
    You can provide default metadata here. AppConfig will override this definition.
    '''
    return {
      'name': 'RedPitaya',
      'description': 'An implementation of RIP to control Red Pitaya',
      'authors': 'Amine my-taj',
      'keywords': 'Red Pitaya, Raspberry PI',
      'readables': [],
      'writables': [],
    }

  def set(self, expid, variables, values):
    '''
    Writes one or more variables to the workspace of the current session
    '''
    # TO DO: do something with variables and values
    pass

  def get(self, expid, variables):
    '''
    Retrieve one or more variables from the workspace of the current session
    '''
    # TO DO: do something with variables and values
    toReturn = {}
    return toReturn

  def getValuesToNotify(self):
    return [
      ['time'],
      [self.sampler.lastTime()]
    ]
