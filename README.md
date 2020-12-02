# rip-python-server
A server implementation of the <a href="https://github.com/UNEDLabs/rip-spec">RIP protocol</a> for online laboratories in Python.

It enables the use of MATLAB and Simulink programs through the Internet as webservices.

Requirements:

Microsoft Visual C++ Compiler for Python 2.7
It is included in the package. Just double click to install it if you need it.

For MATLAB connections: 
Python 2.7
MATLAB r2014b or later --> see https://www.mathworks.com/help/matlab/matlab_external/install-the-matlab-engine-for-python.html
MATLAB and Python must both be the 32 bit version or the 64 bit version.
Matlab engine must be installed. For this, run:
python setup.py install
in matlabroot\extern\engines\python

For Simulink models:
Open your Simulink model, go to Simulation>Pacing and set pacing to 1.
For outputs, connect each Simulink signal you want to monitor from RIP to a "To Workspace" block. Configure the block to store values in array format. It is recommended to configure it to only store the last value too. Make sure the "Log fixed-point data as a fi object" option is unmarked.
Inputs must have a variable associated. For example, a dashboard input must be connected to a constant block and this block must have a variable defined. These variables can be defined either in the model or in the base workspace.
Include these input and output variables in the .json config file, under "writables" and "readables", respectively.
Also include SimulationTime in .json config file as a readable variable.


Use instructions:
In order to run RIP-Matlab.py go to the folder where the file is located and type:
RIP.pyc

You may need to first install all required dependencies:
C:\Python27\Scripts\pip install -r requirements.txt

For this, you may also need to install pip first:
python get-pip.py