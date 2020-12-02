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
from jsonrpc.JsonRpcServer import JsonRpcServer

class JsonRpcServerTest(unittest.TestCase):

  def setUp(self):
    self.builder = JsonRpcBuilder()
    self.server = JsonRpcServer()
    self.server.on('add', {'x', 'y'}, self.add)

  def add(self, x, y):
    return x + y
  
  def testRpcCallWithPositionalParameters(self):
    expected = {'jsonrpc': '2.0', 'result': 65, 'id': 1,}
    response = self.call('add', [42, 23], 1)
    self.assertEqual(ujson.dumps(expected), ujson.dumps(response))

  def call(self, method, params, request_id):
    request = self.builder.request(method, params, request_id);
    response = self.server.parse(ujson.dumps(request))
    return response

  def testRpcCallWithNamedParameters(self):
    expected = {'jsonrpc': '2.0', 'result': 65, 'id': 1,}
    response = self.call('add', {'x':23, 'y':42}, 1);
    self.assertEqual(ujson.dumps(expected), ujson.dumps(response))

  def testRpcCallNonExistentMethod(self):
    expected = {'jsonrpc': '2.0', 'error': self.server.METHOD_NOT_FOUND, 'id': 1,}
    response = self.call('foobar', [], 1)
    self.assertEqual(ujson.dumps(expected), ujson.dumps(response))

  def testRpcCallNotification(self):
    expected = None
    response = self.call('add', [42, 23], None)
    self.assertEqual(expected, response)

  def testRpcCallInvalidJson(self):
    expected = {'jsonrpc': '2.0', 'error': self.server.PARSE_ERROR, 'id': None,}
    request = '{"jsonrpc": "2.0", "method": "foobar, "params": "bar", "baz]'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(expected), ujson.dumps(response))

  def testRpcCallWithInvalidRequestObject(self):
    expected = {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,}
    request = '{"jsonrpc": "2.0"}'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(expected), ujson.dumps(response));

  def testRpcCallBatchWithInvalidJSON(self):
    expected = {'jsonrpc': '2.0', 'error': self.server.PARSE_ERROR, 'id': None,}
    request = '[{"jsonrpc": "2.0", "method": "sum", "params": [1,2,4], "id": "1"}, {"jsonrpc": "2.0", "method"]'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testRpcCallBatchEmptyArray(self):
    expected = {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,}
    request = '[]'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testRpcCallInvalidBatchOne(self):
    expected = [{'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,}]
    request = '[1]'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testRpcCallInvalidBatchThree(self):
    expected = [
      {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,},
      {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,},
      {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None,},
    ]
    request = '[1, 2, 3]'
    response = self.server.parse(request)
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

  def testRpcCallBatch(self):
    expected = [
      {'jsonrpc': '2.0', 'result': 35, 'id': 1},
      {'jsonrpc': '2.0', 'error': self.server.INVALID_REQUEST, 'id': None},
      {'jsonrpc': '2.0', 'error': self.server.METHOD_NOT_FOUND, 'id': 5},
    ]
    request = [
      self.builder.request('add', [23, 12], 1),
      {'jsonrpc':'2.0'},
      self.builder.request('foo.get', [23], 5),
    ]
    response = self.server.parse(ujson.dumps(request))
    self.assertEqual(ujson.dumps(response), ujson.dumps(expected))

#  def testRpcCallBatchAllNotifications(self):
#//rpc call Batch (all notifications):
#//--> [
#//        {"jsonrpc": "2.0", "method": "notify_sum", "params": [1,2,4]},
#//        {"jsonrpc": "2.0", "method": "notify_hello", "params": [7]}
#//    ]
#//<-- //Nothing is returned for all notification batches
#    self.fail('Not Implemented Yet');
