### import ####################################################################


import os
import imp
import collections

import project.project_globals as g
main_dir = g.main_dir.read()
app = g.app.read()
import project.widgets as pw
import project.ini_handler as ini
ini = ini.spectrometers
import project.classes as pc
import hardware.hardware as hw


### driver ####################################################################


class Driver(hw.Driver):
    pass


### gui #######################################################################


class GUI(hw.GUI):
    pass


### hardware ##################################################################


class Hardware(hw.Hardware):
    pass


### initialize ################################################################


# list module path, module name, class name, initialization arguments, friendly name
hardware_dict = collections.OrderedDict()
hardware_dict['MicroHR'] = [os.path.join(main_dir, 'hardware', 'spectrometers', 'MicroHR', 'MicroHR.py'), 'MicroHR', 'MicroHR', [], 'wm']

hardwares = []
for key in hardware_dict.keys():
    if ini.read('hardware', key):
        lis = hardware_dict[key]
        hardware_module = imp.load_source(lis[1], lis[0])
        if g.offline.read():
            hardware_class = getattr(hardware_module, lis[2] + '_offline')
        else:
            hardware_class = getattr(hardware_module, lis[2])
        hardware_obj = Hardware(hardware_class, lis[3], Driver, key, True, lis[4])
        hardwares.append(hardware_obj)

gui = pw.HardwareFrontPanel(hardwares, name='Spectrometers')
advanced_gui = pw.HardwareAdvancedPanel(hardwares, gui.advanced_button)

