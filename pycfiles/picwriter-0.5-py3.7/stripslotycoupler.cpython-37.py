# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\picwriter\components\stripslotycoupler.py
# Compiled at: 2019-03-25 19:18:03
# Size of source mod 2**32: 6235 bytes
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np, gdspy
import picwriter.toolkit as tk

class StripSlotYCoupler(gdspy.Cell):
    __doc__ = " Strip-to-Slot Y-Coupler Cell class (subclass of gdspy.Cell).  For more information on this specific type of strip to slot mode converter, please see the original paper at https://doi.org/10.1364/OL.34.001498.\n\n        Args:\n           * **wgt_input** (WaveguideTemplate):  WaveguideTemplate object for the input waveguide (should be either of type `strip` or `slot`).\n           * **wgt_output** (WaveguideTemplate):  WaveguideTemplate object for the output waveguide (should be either of type `strip` or `slot`, opposite of the input type).\n           * **length** (float): Length of the tapered region.\n           * **d** (float): Distance between the outer edge of the strip waveguide and the start of the slot waveguide rail.\n\n        Keyword Args:\n           * **end_strip_width** (float): End width of the strip waveguide (at the narrow tip).  Defaults to 0.\n           * **end_slot_width** (float): End width of the slot waveguide (at the narrow tip).  Defaults to 0.\n           * **input_strip** (Boolean): If `True`, sets the input port to be the strip waveguide side.  If `False`, slot waveguide is on the input.  Defaults to `None`, in which case the input port waveguide template is used to choose.\n           * **port** (tuple): Cartesian coordinate of the input port.  Defaults to (0,0).\n           * **direction** (string): Direction that the component will point *towards*, can be of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, OR an angle (float, in radians)\n\n        Members:\n           * **portlist** (dict): Dictionary with the relevant port information\n\n        Portlist format:\n           * portlist['input'] = {'port': (x1,y1), 'direction': 'dir1'}\n           * portlist['output'] = {'port': (x2, y2), 'direction': 'dir2'}\n\n        Where in the above (x1,y1) is the same as the 'port' input, (x2, y2) is the end of the taper, and 'dir1', 'dir2' are of type `'NORTH'`, `'WEST'`, `'SOUTH'`, `'EAST'`, *or* an angle in *radians*.\n        'Direction' points *towards* the waveguide that will connect to it.\n\n        Note: The waveguide and cladding layer/datatype are taken from the `wgt_slot` by default.\n\n    "

    def __init__(self, wgt_input, wgt_output, length, d, end_strip_width=0, end_slot_width=0, input_strip=None, port=(0, 0), direction='EAST'):
        gdspy.Cell.__init__(self, tk.getCellName('StripSlotYCoupler'))
        self.portlist = {}
        if not isinstance(input_strip, bool):
            if input_strip != None:
                raise ValueError('Invalid input provided for `input_strip`.  Please specify a boolean.')
        elif input_strip == None:
            self.input_strip = wgt_input.wg_type == 'strip' or wgt_input.wg_type == 'swg'
        else:
            self.input_strip = input_strip
        if self.input_strip:
            self.wgt_strip = wgt_input
            self.wgt_slot = wgt_output
        else:
            self.wgt_strip = wgt_output
            self.wgt_slot = wgt_input
        self.wg_spec = {'layer':wgt_output.wg_layer, 
         'datatype':wgt_output.wg_datatype}
        self.clad_spec = {'layer':wgt_output.clad_layer,  'datatype':wgt_output.clad_datatype}
        self.length = length
        self.d = d
        self.end_strip_width = end_strip_width
        self.end_slot_width = end_slot_width
        self.port = port
        self.trace = [port, tk.translate_point(port, length, direction)]
        self.direction = direction
        self.build_cell()
        self.build_ports()

    def build_cell(self):
        angle = tk.get_exact_angle(self.trace[0], self.trace[1])
        angle_opp = tk.get_exact_angle(self.trace[1], self.trace[0])
        path_strip = gdspy.Path(self.wgt_strip.wg_width, self.trace[0])
        (path_strip.segment)(self.length, final_width=self.end_strip_width, direction=angle, **self.wg_spec)
        path_slot = gdspy.Path((self.wgt_slot.rail), (self.trace[1]), number_of_paths=2, distance=(self.wgt_slot.rail_dist))
        (path_slot.segment)(self.length, final_width=self.end_slot_width, final_distance=self.wgt_strip.wg_width + 2 * self.d + self.end_slot_width, direction=angle_opp, **self.wg_spec)
        path_clad = gdspy.Path(2 * self.wgt_strip.clad_width + self.wgt_strip.wg_width, self.trace[0])
        (path_clad.segment)(self.length, final_width=2 * self.wgt_slot.clad_width + self.wgt_slot.wg_width, direction=angle, **self.clad_spec)
        if not self.input_strip:
            center_pt = (
             (self.trace[0][0] + self.trace[1][0]) / 2.0, (self.trace[0][1] + self.trace[1][1]) / 2.0)
            path_strip.rotate(np.pi, center_pt)
            path_slot.rotate(np.pi, center_pt)
            path_clad.rotate(np.pi, center_pt)
        self.add(path_strip)
        self.add(path_slot)
        self.add(path_clad)

    def build_ports(self):
        self.portlist['input'] = {'port':self.trace[0], 
         'direction':tk.flip_direction(self.direction)}
        self.portlist['output'] = {'port':self.trace[1],  'direction':self.direction}


if __name__ == '__main__':
    from . import *
    top = gdspy.Cell('top')
    wgt_slot = WaveguideTemplate(bend_radius=50, wg_type='strip', wg_width=0.7)
    wgt_strip = WaveguideTemplate(bend_radius=50, wg_type='slot', wg_width=0.7, slot=0.2)
    wg1 = Waveguide([(0, 0), (100, 100)], wgt_strip)
    tk.add(top, wg1)
    ycoup = StripSlotYCoupler(wgt_strip, wgt_slot, 10.0, 0.2, end_slot_width=0.1, **wg1.portlist['output'])
    tk.add(top, ycoup)
    x1, y1 = ycoup.portlist['output']['port']
    wg2 = Waveguide([(x1, y1), (x1 + 100, y1 + 100)], wgt_slot)
    tk.add(top, wg2)
    gdspy.LayoutViewer(cells=top)