# This file contains the configuration of the RIP server application.
config = {
  # TO DO: The server will listen to host:port
  'server': {
    'host': '127.0.0.1',
    'port': 8080,
  },
  # The 'control' section configures the mapping between the RIP protocol
  # and the actual implementation of the functionality.
  # The 'impl' field should contain the name of the module (.py) and the
  # class that implement the control interface
  'control': {
    'impl_module': 'RIPRedPitaya',
    'info': {
      'name': 'RedPitaya',
      'description': 'An implementation of RIP to control Red Pitaya',
      'authors': 'Amine my-taj',
      'keywords': 'Red Pitaya, Raspberry PI',
      'readables': [],
      'writables': [],
    }
  }
}
