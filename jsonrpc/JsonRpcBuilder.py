# JSON-RPC Builder
# author: Jesus Chacon <jcsombria@gmail.com>
#
# Copyright (C) 2013 Jesus Chacon
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

class JsonRpcBuilder(object):
  """A helper class to build JSON-RPC v2.0 objects."""
  def request(self, method, params=None, request_id=None):
    request = {
      'jsonrpc': '2.0',
      'method': method,
    }
    if(params != None):
      request['params'] = params
    if(request_id != None):
      request['id'] = request_id
    return request

  def response(self, result, request_id=None):
    ''' Build a jsonrpc response object
    '''
    if(request_id != None):
      return {
        'jsonrpc': '2.0',
        'result': result,
        'id': request_id
      }
    else:
      return {
        'jsonrpc': '2.0',
        'result': result,
      }

  def error_response(self, error, request_id=None):
    ''' Build a jsonrpc error response object
    '''
    return {
      'jsonrpc': '2.0',
      'error': error,
      'id': request_id
    }

  def error(self, code, message, data=None):
    ''' Build a jsonrpc error object
    '''
    if(data != None):
      return {
        'code': code,
        'message': message,
        'data': data
      }
    else:
      return {
        'code': code,
        'message': message,
      }

  def parseResponse(self, message):
    response = None
    try:
      response = ujson.loads(message);
    except ValueError:
      print(error);
    return response.get('result') if response != None else None
