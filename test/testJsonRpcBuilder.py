# JSON-RPC Builder Tester
# author: Jesús Chacón <jcsombria@gmail.com>
#
# Copyright (C) 2013 Jesús Chacón
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import ujson
import unittest
from jsonrpc.JsonRpcBuilder import JsonRpcBuilder

class JsonRpcBuilderTest(unittest.TestCase):

  def setUp(self):
    self.builder = JsonRpcBuilder()
    
  def testRequest(self): 
    expected = {'jsonrpc':'2.0', 'method':'testMethod', 'params':['testParam'], 'id':'test_id'}
    request = self.builder.request('testMethod', ['testParam'], "test_id")
    self.assertEqual(ujson.dumps(request), ujson.dumps(expected))

  def testResponse(self):
    expected = {'jsonrpc':'2.0', 'result':12.43, 'id':'test_response'}
    response = self.builder.response(12.43, 'test_response')
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testResponseWithError(self):
    expected = {'jsonrpc':'2.0', 'error':'Test Error', 'id':'test_error'}
    response = self.builder.error_response('Test Error', 'test_error')
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testParseResponse(self):
    response = '{"jsonrpc":"2.0","result":12.43,"id":"test_parse"}'
    expected = 12.43
    result = self.builder.parseResponse(response)
    self.assertEqual(expected, result)
