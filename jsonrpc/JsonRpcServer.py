# JSON-RPC Server
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
from .JsonRpcBuilder import JsonRpcBuilder

class JsonRpcServer(object):
  """Base class for defining a JSON-RPC v2.0 server."""

  name = 'jsonrpcserver'

  PARSE_ERROR = {
    'code': -32700,
    'message': 'Invalid JSON was received by the server.',
  }
  INVALID_REQUEST = {
    'code': -32600,
    'message': 'The JSON sent is not a valid Request object.',
  }
  METHOD_NOT_FOUND = {
    'code': -32601,
    'message': 'Method not found. The method does not exist / is not available.',
  }
  INVALID_PARAMS = {
    'code': -32602,
    'message': 'Invalid params',
  }
  INTERNAL_ERROR = {
    'code': -32603,
    'message':'Internal JSON-RPC error.',
  }
  ERRORS = {
    'PARSE_ERROR': PARSE_ERROR,
    'INVALID_REQUEST': INVALID_REQUEST,
    'METHOD_NOT_FOUND': METHOD_NOT_FOUND,
    'INVALID_PARAMS': INVALID_PARAMS,
    'INTERNAL_ERROR': INTERNAL_ERROR,
    # -32000 to -32099 server error:
    #   Reserved for implementation-defined server-errors.
  }

  def __init__(self, name='JsonRpcServer', description='A good-looking and nice jsonrpc server for python.'):
    self.name = name
    self.description = description
    self.builder = JsonRpcBuilder()
    self.methods = {}

  def parse(self, jsonrpc):
    try:
      methodCall = ujson.loads(jsonrpc)
    except ValueError:
      return self._response_with_error('PARSE_ERROR')
    isBatchMode = isinstance(methodCall, list)
    if(isBatchMode):
      if(len(methodCall) == 0):
        return self._response_with_error('INVALID_REQUEST')
      result = []
      for request in methodCall:
        response = self.process(request)
        if(response):
          result.append(response)
    else:
      result = self.process(methodCall)
    return ujson.dumps(result)

  def process(self, request):
    """ Process a JSON-RPC request:
      if the method exists in the server, invoke and return the result.
      if not, an error is returned.
    """
    request_id = None
    try:
      (method, params, request_id) = self._check_fields(request)
      server_method = self.methods.get(method)
      if not server_method:
        raise InvocationException('METHOD_NOT_FOUND')
      result = self._invoke(server_method, params)
      if request_id:
        return self.builder.response(result, request_id)
    except InvocationException as error:
      return self._response_with_error(error.code, request_id)

  def _check_fields(self, request):
    # jsonrpc must be 2.0, method must always exists. 'id' and 'params' may be omitted
    try:
      jsonrpc = request['jsonrpc']
      method = request['method']
      request_id = request.get('id')
      params = request.get('params')
    except:
      raise InvocationException('INVALID_REQUEST')

    return (method, params, request_id)

  def _invoke(self, method, params):
    if not method:
      raise InvocationException('METHOD_NOT_FOUND')
    return method.invoke(params)

  def _response_with_error(self, error_name, request_id=None):
    error_info = self.ERRORS[error_name]
    error = self.builder.error(
      error_info['code'],
      error_info['message'],
    )
    return self.builder.error_response(error, request_id)

  def on(self, method, expected, handler):
    if not isinstance(expected, (int, dict)):
      return False
    self.methods[method] = Method(method, handler, expected)

  def info(self):
    return { 'info': [{
      'name': self.name,
      'description': self.description,
      'methods': self.getMethods(),
      'readable': {},
      'writable': {},
      }]
    }

  def getMethods(self):
    methodList = [method.info() for method in self.methods.values()]
    return methodList

  def addMethods(self, methods):
    for m in methods:
      try:
        implementation = methods[m].get('implementation')
        self.on(m, methods[m], implementation)
      except:
        print('[WARNING] Ignoring invalid method')

class InvocationException(Exception):
  """Exception raised for an error occurred during the invocation of a method
  Attributes:
    code -- an code describing the error
  """
  def __init__(self, code):
    self.code = code


class Method(object):
  """Helper class to invoke a method and check the validity of the params
  """
  def __init__(self, name, handler, info):
    self._name = name
    self._handler = handler
    self._info = info
    self._params = info.get('params')
    self._description = info.get('description')

  def invoke(self, params):
    if not self._expect_params():
      return self._handler()
    elif self._check_params_by_position(params):
      return self._handler(*params)
    elif self._check_params_by_name(params):
      return self._handler(**params)
    raise InvocationException('INVALID_PARAMS')

  def info(self):
    if(self._params == None):
      params = {}
    else:
      params = self._params
    return {
      'method': self._name,
      'description': self._description,
      'params': params,
      'return': '[]',
    }

  def _expect_params(self):
    try:
      return self._params != None and not self._params == 0
    except:
      return False

  def _check_params_by_position(self, params):
    try:
      expectedByPosition = len(self._params)
    except:
      expectedByPosition = self._params
    return expectedByPosition == 0 or (isinstance(params, list) and len(params) == expectedByPosition)

  def _check_params_by_name(self, params):
    for name in params:
      if name not in self._params:
        return False
    return True