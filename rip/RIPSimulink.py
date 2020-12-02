"""
@author: jcsombria
"""
from rip.RIPGeneric import RIPGeneric
from rip.matlabconn.MatlabConnector import MatlabConnector


class RIPSimulink(RIPGeneric):
    """
    RIP MATLAB Adapter
    """

    def __init__(self, info):
        """
        Constructor
        """
        super(RIPSimulink, self).__init__(info)
        self.simulink = MatlabConnector()

        self.simulink.connect()
        self.simulink.open(info['model'])

    def default_info(self):
        """
        Default metadata.
        """
        return {
          'name': 'Simulink',
          'description': 'An implementation of RIP to control a MATLAB/SIMULINK model',
          'authors': 'J. Chacon',
          'keywords': 'MATLAB, SIMULINK',
          'readables': [],
          'writables': [],
        }

    def set(self, expid, variables, values):
        self.simulink.set(variables, values)

    def beforeRun(self):
        if not self.simulink.started:
            self.simulink.start()
            self.simulink.creatertos(self._getReadables())
            print("Control started")

    def preGetValuesToNotify(self):
        pass

    def getValuesToNotify(self, expid=None):
        return self.simulink.get(self._getReadables())

    def postGetValuesToNotify(self):
        pass

    def stop(self):
        self.simulink.started = False
        self.simulink.stop()

    def exitThis(self):
        self.simulink.close_system()
        self.simulink.exit()
