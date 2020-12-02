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
    'impl_module': 'RIPGeneric',
    # Also, if the class name is not the same as the module name:
    #'impl_name': 'RIPGeneric',
    'info': {
      'name': 'RIP Generic',
      'description': 'A generic implementation of RIP',
      'authors': 'J. Chacon',
      'keywords': 'Raspberry PI, RIP',
      # Server readable objects
      'readables': [{
        'name':'time',
        'description':'Server time in seconds',
        'type':'float',
        'min':'0',
        'max':'Inf',
        'precision':'0'
      }],
      # Server writable objects
      'writables': []
    },
  }
}
