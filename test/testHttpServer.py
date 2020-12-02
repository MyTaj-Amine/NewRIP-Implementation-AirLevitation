import urllib3
import sys

if __name__ == '__main__':
  pool = urllib3.PoolManager()
  serverUrl = 'http://localhost:2055'
  headers = {'Content-Type':'application/json'}
  methodCall = [
    '{ "jsonrpc":"2.0", "method":"connect", "params":[], "id":"1" }',
#    '{ "jsonrpc":"2.0", "method":"step", "params":[[0.01]], "id":"1" }',
#    '{ "jsonrpc":"2.0", "method":"disconnect", "params":[], "id":"1" }',
  ]
  for method in methodCall:
    response = pool.urlopen('POST', serverUrl, headers = headers, body = method)
    print(response.data)
    response.close()

'''
from websocket import create_connection
import time

ws = create_connection('ws://localhost:9000/ws')
for method in methodCall:
  print(result)
  ws.send(method)
  time.sleep(5)
  result = ws.recv()
ws.close()
'''