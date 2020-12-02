'''
Created on 20/10/2015

@author: jcsombria
'''
import unittest
import ujson

from app.RIPMatlab import RIPMatlab
from jsonrpc.JsonRpcBuilder import JsonRpcBuilder


class RIPMatlabTest(unittest.TestCase):


  def setUp(self):
    self.builder = JsonRpcBuilder()
    self.matlab = RIPMatlab()

  def tearDown(self):
    pass


  def testName(self):
    request = self.builder.request('connect', params=None, request_id='1')
    result = self.matlab.parse(ujson.dumps(request))
    request = self.builder.request('connect', params=[], request_id='1')
    result = self.matlab.parse(ujson.dumps(request))
    print(result)
    request = self.builder.request('get', params=[['x','y']], request_id='2')
    result = self.matlab.parse(ujson.dumps(request))
    print(result)
    request = self.builder.request('set', params=[['x','y'], [12, 7]])
    result = self.matlab.parse(ujson.dumps(request))
    print(result)
    request = self.builder.request('eval', params=['y=2*x;'])
    result = self.matlab.parse(ujson.dumps(request))
    print(result)
    request = self.builder.request('get', params=[['x','y']], request_id='2')
    result = self.matlab.parse(ujson.dumps(request))
    print(result)
    


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()