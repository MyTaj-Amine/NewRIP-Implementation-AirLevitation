import matlab.engine

if __name__ == '__main__':
  _matlab = matlab.engine.start_matlab('-desktop')
  try:
    result = _matlab.eval('y=1;', nargout=0)
  except:
    pass
  print(result)
