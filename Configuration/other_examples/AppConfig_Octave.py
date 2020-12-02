# This file contains the configuration of the RIP server application.
config = {
  'server': {
    'host': '127.0.0.1',
    'port': 8080,
  },
  # The 'control' section configures the mapping between the RIP protocol
  # and the actual implementation of the functionality.
  # The 'impl' field should contain the name of the module (.py) and the
  # class that implement the control interface
  'control': {
    'impl_module': 'RIPOctave',
    # Also, if the class name is not the same as the module name:
    #'impl_name': 'RIPOctave',
    'info': {
      'name': 'Octave',
      'description': 'An implementation of RIP to control Octave',
      'authors': 'D. Garcia, J. Chacon',
      'keywords': 'Octave, Raspberry PI, Robot',
      # Server readable objects
      'readables': [{
        'name':'x',
        'description':'Testing readable variable',
        'type':'float',
        'min':'-Inf',
        'max':'Inf',
        'precision':'0'
      }],
      # Server writable objects
      'writables': [{
        'name':'x',
        'description':'Testing readable variable',
        'type':'float',
        'min':'-Inf',
        'max':'Inf',
        'precision':'0'
      }],
    },
  }
}
