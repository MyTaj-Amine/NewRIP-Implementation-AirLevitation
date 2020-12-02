# Matlab MatlabConnector Tester
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
import unittest
from rip.matlab.MatlabConnector import MatlabConnector
import time


class MatlabConnectorTest(unittest.TestCase):

    def setUp(self):
        self.matlab = MatlabConnector()

    def testOpen(self):
        self.matlab.connect()
        self.matlab.open('./examples/EjemploPulso.slx')
        time.sleep(5)
        self.matlab.step()
        time.sleep(5)


# class CommandBuilderTest(unittest.TestCase):

#  def setUp(self):
#    self.builder = CommandBuilder() 

#  def testCD(self):
#    path = '/home/test/test.mdl'
#    expected = 'cd (\'/home/test\');'
#    result = self.builder.cd(path)
#    self.assertEqual(result, expected)

#  def testSetParam(self):
#    model = 'test'
#    param = 'SimulationCommand'
#    value = 'start'
#    expected = 'set_param (\'test\', \'SimulationCommand\', \'start\');'
#    result = self.builder.set_param(model, param, value)
#    self.assertEqual(result, expected)

#  def testLoadSystem(self):
#    path = '/home/test'
#    expected = 'cd (\'/home/test\');'
#    result = self.builder.cd(path)
#    self.assertEqual(result, expected)
