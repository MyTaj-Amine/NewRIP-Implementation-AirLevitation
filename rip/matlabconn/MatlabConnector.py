# CommandBuilder
# author: Jesus Chacon <jcsombria@gmail.com>
#
# Copyright (C) 2014 Jesus Chacon
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
import os.path
import matlab.engine
import numpy as np
from CommandBuilder import CommandBuilder
from QuarcTCPClient import QuarcTCPClient


class MatlabConnector(object):

    def __init__(self):
        self.started = False
        self.matlab = None
        self.quarc = True
        self.external = True
        self.build = True
        self.external = self.quarc & self.external
        self.build = self.quarc & self.build
        self.commandBuilder = CommandBuilder()

    def connect(self):
        if self.matlab == None:
            names = matlab.engine.find_matlab()
            if not names:
                # self.matlab = matlab.engine.start_matlab()  # use matlab.engine.start_matlab('-desktop') for debug
                try:
                    future = matlab.engine.start_matlab(async=True)  # use async=True in old versions
                except:
                    future = matlab.engine.start_matlab(background=True)  # use background=True for async
                self.matlab = future.result()
                print("Opened new MATLAB session")
            else:
                # self.matlab = matlab.engine.connect_matlab(names[0])  # TODO: Control which shared session connect to?
                try:
                    future = matlab.engine.connect_matlab(names[0], async=True)
                except:
                    future = matlab.engine.connect_matlab(names[0], background=True)
                self.matlab = future.result()
                print("Connected to existing MATLAB session: " + names[0])

    def stop(self):
        self._stop(self.model['name'])

    def disconnect(self):
        self._stop(self.model['name'])
        self._close_system(self.model['name'])
        self._exitThis()

    def set(self, variables, values):
        if isinstance(variables, list):
            size = len(variables)
            for i in range(size):
                try:
                    name, value = variables[i], values[i]
                    tomodelworkspace = self.commandBuilder.to_model_workspace(name, value)
                    try:
                        self.matlab.eval(tomodelworkspace, async=True, nargout=0)
                    except:
                        self.matlab.eval(tomodelworkspace, background=True, nargout=0)
                except:
                    pass
        else:
            try:
                name, value = variables, values
                tomodelworkspace = self.commandBuilder.to_model_workspace(name, value)
                try:
                    self.matlab.eval(tomodelworkspace, async=True, nargout=0)
                except:
                    self.matlab.eval(tomodelworkspace, background=True, nargout=0)
            except:
                pass
        self._update(self.model['name'])

    def get(self, variables):
        future_value = {}
        variables_names = []
        variables_values = []
        if self.external:
            data = self.qtcpc.read(variables)
            for name in variables:
                try:
                    variables_names.append(name)
                    variables_values.append(data[name])
                except:
                    pass
        else:
            for name in variables:
                try:
                    if name == "SimulationTime":
                        try:
                            future_value[name] = self.matlab.get_param(self.model['name'], name, background=True)
                        except:
                            future_value[name] = self.matlab.get_param(self.model['name'], name, async=True)
                    else:
                        try:
                            future_value[name] = self.matlab.eval(name + '.InputPort(1).Data', background=True)
                        except:
                            future_value[name] = self.matlab.eval(name + '.InputPort(1).Data', async=True)
                except:
                    pass
            for name in variables:
                try:
                    variables_names.append(name)
                    if name == "SimulationTime":
                        variables_values.append(future_value[name].result())
                    else:
                        variables_values.append(future_value[name].result())
                except:
                    pass
        return np.array([variables_names, variables_values]).tolist()

    def open(self, path):
        """"
        Open a Simulink model
        """
        try:
            dirname = os.path.dirname(path)
            filename = os.path.basename(path)
            modelname = os.path.splitext(filename)[0]
            self.model = {
                'path': dirname,
                'file': filename,
                'name': modelname,
            }
            version = self.matlab.version('-release')
            if version >= '2018b':
                self.matlab.eval('Simulink.sdi.setAutoArchiveMode(false);', nargout=0)
                self.matlab.eval('Simulink.sdi.setArchiveRunLimit(0);', nargout=0)
            self._load(self.model)
            self._settime(self.model['name'])
            self._getmodelworkspace(self.model['name'])
            self._buildandconnect(self.model['name'])  # for quarc only
        except:
            print("Could not open simulink model " + path)

    def close_system(self):
        self._close_system(self.model['name'])

    def exit(self):
        self._exitThis()

    def _load(self, model):
        version = self.matlab.version('-release')
        self.matlab.cd(model['path'])
        autosavedfile = model['file'] + '.autosave'
        cachedfile = model['file'] + 'c'
        if version >= '2017b':
            if self.matlab.isfile(autosavedfile):
                self.matlab.delete(autosavedfile, nargout=0)
            if self.matlab.isfile(cachedfile):
                self.matlab.delete(cachedfile, nargout=0)
        else:
            if self.matlab.exist(autosavedfile, 'file') == 2:
                self.matlab.delete(autosavedfile, nargout=0)
            if self.matlab.exist(cachedfile, 'file') == 2:
                self.matlab.delete(cachedfile, nargout=0)
        if version >= '2018b':
            if not self.matlab.slreportgen.utils.isModelLoaded(model['name']):
                self.matlab.load_system(model['file'])
        else:
            self.matlab.load_system(model['file'])
        print("Loaded Simulink model")

    def _getmodelworkspace(self, model):
        getmodelworkspace = self.commandBuilder.get_model_workspace(model)
        self.matlab.eval(getmodelworkspace, nargout=0)

    def _settime(self, model):
        self.matlab.set_param(model, "StartTime", "0", nargout=0)
        self.matlab.set_param(model, "StopTime", "inf", nargout=0)
        self.matlab.set_param(model, 'SolverType', 'Fixed-step', nargout=0)
        if not self.external:
            self.matlab.set_param(model, 'FixedStep', '0.06', nargout=0)

    def start(self):
        if self.quarc:
            if self.external:
                self.matlab.qc_set_simulation_mode(self.model['name'], 'external', nargout=0)
            else:
                self.matlab.qc_set_simulation_mode(self.model['name'], 'normal', nargout=0)
            self.matlab.qc_start_model(self.model['name'], async=True, nargout=0)
        else:
            try:
                self.matlab.qc_set_simulation_mode(self.model['name'], 'normal', nargout=0)
            except:
                pass
            self.matlab.set_param(self.model['name'], "SimulationCommand", "start", async=True, nargout=0)
        self.started = True

    def creatertos(self, readables):
        if self.external:
            self.qtcpc = QuarcTCPClient(18000)
            self.qtcpc.config(['double'] * len(readables))  # TODO: Add support for other data types
        else:
            for readable in readables:
                if readable != "SimulationTime":
                    try:
                        self.matlab.eval(readable + "=get_param('" + self.model['name'] + "/" + readable +
                                         "', 'RuntimeObject');", async=True, nargout=0)
                    except:
                        self.matlab.eval(readable + "=get_param('" + self.model['name'] + "/" + readable +
                                         "', 'RuntimeObject');", background=True, nargout=0)

    def _pause(self, model):
        self.matlab.set_param(model, "SimulationCommand", "pause", nargout=0)

    def ispaused(self):
        return self.matlab.get_param(self.model['name'], "SimulationStatus")

    def _buildandconnect(self, model):
        self.matlab.set_param(model, 'AccelVerboseBuild', 'off', nargout=0)
        self.matlab.save_system(model, nargout=0)
        try:
            if self.external:
                if self.build:
                    self.matlab.qc_build_model(model, nargout=0)
                    print("Quarc model has been built")
                if not self.matlab.qc_is_model_loaded(model):
                    self.matlab.qc_download_model(model, nargout=0)
                    print("Quarc model downloaded in target")
                    self.matlab.qc_load_model(model, nargout=0)
                    print("Quarc model loaded in target")
                self.matlab.qc_connect_model(model, nargout=0)
                print("Simulink model connected to quarc target")
        except:
            pass

    def _update(self, model):
        if self.external:
            try:
                self.matlab.qc_update_model(model, async=True, nargout=0)
            except:
                self.matlab.qc_update_model(model, background=True, nargout=0)
        else:
            try:
                self.matlab.set_param(model, "SimulationCommand", "update", async=True, nargout=0)
            except:
                self.matlab.set_param(model, "SimulationCommand", "update", background=True, nargout=0)

    def resume(self):
        try:
            self.matlab.set_param(self.model['name'], "SimulationCommand", "continue", async=True, nargout=0)
        except:
            self.matlab.set_param(self.model['name'], "SimulationCommand", "continue", background=True, nargout=0)

    def _stop(self, model):
        if self.external:
            self.qtcpc.close()
            self.matlab.qc_stop_model(model)
            self.matlab.qc_connect_model(model, nargout=0)
        else:
            self.matlab.set_param(model, "SimulationCommand", "stop", nargout=0)
        self.started = False

    def _close_system(self, model):
        self.matlab.close_system(model)

    def _exitThis(self):
        self.qtcpc.close()
        self.matlab.quit()
