# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/software_modules/lockbox/output.py
# Compiled at: 2017-08-29 09:44:06
from __future__ import division
import numpy as np
from scipy import interpolate
from ...software_modules.lockbox.input import Signal
from ...attributes import BoolProperty, FloatProperty, SelectProperty, FilterProperty, FrequencyProperty, IntProperty
from ...curvedb import CurveDB
from ...hardware_modules.asg import Asg0, Asg1
from ...hardware_modules.pid import Pid
from ...widgets.module_widgets import OutputSignalWidget

class AdditionalFilterAttribute(FilterProperty):

    def valid_frequencies(self, obj):
        return obj.pid.__class__.inputfilter.valid_frequencies(obj.pid)

    def get_value(self, obj):
        return obj.pid.inputfilter

    def set_value(self, obj, value):
        obj.pid.inputfilter = value
        obj.lockbox._signal_launcher.update_transfer_function.emit([obj])


class OutputSignal(Signal):
    """
    As many output signals as desired can be added to the lockbox. Each
    output defines:
      - name: the name of the output.
      - dc_gain: how much the model's variable is expected to change for 1 V
        on the output (in *unit*)
      - unit: see above, should be one of the units available in the model.
      - sweep_amplitude/offset/frequency/waveform: what properties to use when
        sweeping the output
      - output_channel: what physical output is used.
      - p/i: the gains to use in a loop: those values are to be understood as
        full loop gains (p in [1], i in [Hz])
      - additional_filter: a filter (4 cut-off frequencies) to add to the loop
        (in sweep and lock mode)
      - extra_module: extra module to add just before the output (usually iir).
      - extra_module_state: name of the state to use for the extra_module.
      - tf_curve: the index of the curve describing the analog transfer
        function behind the output.
      - tf_filter: alternatively, the analog transfer function can be specified
        by a filter (4 cut-off frequencies).
      - desired_unity_gain_frequency: desired value for unity gain frequency.
      - tf_type: ["flat", "curve", "filter"], how is the analog transfer
        function specified.
    """
    _widget_class = OutputSignalWidget
    _gui_attributes = ['unit',
     'sweep_amplitude',
     'sweep_offset',
     'sweep_frequency',
     'sweep_waveform',
     'dc_gain',
     'output_channel',
     'p',
     'i',
     'additional_filter',
     'analog_filter_cutoff',
     'extra_module',
     'extra_module_state',
     'desired_unity_gain_frequency',
     'max_voltage',
     'min_voltage']
    _setup_attributes = _gui_attributes + ['assisted_design', 'tf_curve',
     'tf_type']
    dc_gain = FloatProperty(default=1.0, min=-10000000000.0, max=10000000000.0, call_setup=True)
    output_channel = SelectProperty(options=['out1', 'out2',
     'pwm0', 'pwm1'])
    unit = SelectProperty(default='V/V', options=lambda inst: [ u + '/V' for u in inst.lockbox._output_units ], call_setup=True, ignore_errors=True)
    tf_type = SelectProperty(['flat', 'filter', 'curve'], default='filter', call_setup=True)
    tf_curve = IntProperty(call_setup=True)
    sweep_amplitude = FloatProperty(default=1.0, min=-1, max=1, call_setup=True)
    sweep_offset = FloatProperty(default=0.0, min=-1, max=1, call_setup=True)
    sweep_frequency = FrequencyProperty(default=50.0, call_setup=True)
    sweep_waveform = SelectProperty(options=Asg1.waveforms, default='ramp', call_setup=True)
    assisted_design = BoolProperty(default=True, call_setup=True)
    desired_unity_gain_frequency = FrequencyProperty(default=100.0, min=0, max=10000000000.0, call_setup=True)
    analog_filter_cutoff = FrequencyProperty(default=0, min=0, max=10000000000.0, increment=0.1, call_setup=True)
    p = FloatProperty(min=-10000000000.0, max=10000000000.0, call_setup=True)
    i = FloatProperty(min=-10000000000.0, max=10000000000.0, call_setup=True)
    additional_filter = AdditionalFilterAttribute()
    extra_module = SelectProperty(['None', 'iir', 'pid', 'iq'], call_setup=True)
    extra_module_state = SelectProperty(options=['None'], call_setup=True)
    current_state = SelectProperty(options=['lock', 'unlock', 'sweep'], default='unlock')
    max_voltage = FloatProperty(default=1.0, min=-1.0, max=1.0, call_setup=True, doc='positive saturation voltage')
    min_voltage = FloatProperty(default=-1.0, min=-1.0, max=1.0, call_setup=True, doc='negative saturation voltage')

    def signal(self):
        return self.pid.name

    @property
    def pid(self):
        if not hasattr(self, '_pid') or self._pid is None:
            self._pid = self.pyrpl.pids.pop(self.name)
            self._setup_pid_output()
        return self._pid

    @property
    def is_saturated(self):
        """
        Returns
        -------
        True: if the output has saturated
        False: otherwise
        """
        ival, max, min = self.pid.ival, self.max_voltage, self.min_voltage
        sample = getattr(self.pyrpl.rp.sampler, self.pid.name)
        if (ival > max or ival < min) and (sample > max or sample < min):
            return True
        return False

    def _setup_pid_output(self):
        self.pid.max_voltage = self.max_voltage
        self.pid.min_voltage = self.min_voltage
        if self.output_channel.startswith('out'):
            self.pid.output_direct = self.output_channel
            for pwm in [self.pyrpl.rp.pwm0, self.pyrpl.rp.pwm1]:
                if pwm.input == self.pid.name:
                    pwm.input = 'off'

        elif self.output_channel.startswith('pwm'):
            self.pid.output_direct = 'off'
            pwm = getattr(self.pyrpl.rp, self.output_channel)
            pwm.input = self.pid
        else:
            raise NotImplementedError("Selected output_channel '%s' is not implemented" % self.output_channel)

    def _clear(self):
        """
        Free up resources associated with the output
        """
        self.pyrpl.pids.free(self.pid)
        self._pid = None
        super(OutputSignal, self)._clear()
        return

    def unlock(self, reset_offset=False):
        self.pid.p = 0
        self.pid.i = 0
        if reset_offset:
            self.pid.ival = 0
        self.current_state = 'unlock'
        self._setup_pid_output()

    def sweep(self):
        self.unlock(reset_offset=True)
        self.pid.input = self.lockbox.asg
        self.lockbox.asg.setup(amplitude=self.sweep_amplitude, offset=self.sweep_offset, frequency=self.sweep_frequency, waveform=self.sweep_waveform, trigger_source='immediately', cycles_per_burst=0)
        self.pid.setpoint = 0.0
        self.pid.p = 1.0
        self.current_state = 'sweep'

    def lock(self, input=None, setpoint=None, offset=None, gain_factor=None):
        """
        Closes the lock loop, using the required p and i parameters.
        """
        self._lock_input = self._lock_input if input is None else input
        self._lock_setpoint = self._lock_setpoint if setpoint is None else setpoint
        self._lock_gain_factor = self._lock_gain_factor if gain_factor is None else gain_factor
        self._setup_pid_lock(input=self._lock_input, setpoint=self._lock_setpoint, offset=offset, gain_factor=self._lock_gain_factor)
        self.current_state = 'lock'
        return

    def _setup_pid_lock(self, input, setpoint, offset=None, gain_factor=1.0):
        """
        If current mode is "lock", updates the gains of the underlying pid module such that:
            - input.gain * pid.p * output.dc_gain = output.p
            - input.gain * pid.i * output.dc_gain = output.i
        """
        if isinstance(input, str):
            input = self.lockbox.inputs[input]
        output_unit = self.unit.split('/')[0]
        external_loop_gain = self.dc_gain * self.lockbox._unit_in_setpoint_unit(output_unit)
        external_loop_gain *= input.expected_slope(setpoint)
        if external_loop_gain == 0:
            self._logger.warning('External loop gain for output %s is zero. Skipping pid lock for this step. ', self.name)
        else:
            self.pid.setpoint = input.expected_signal(setpoint) + input.calibration_data._analog_offset
            self.pid.p = self.p / external_loop_gain * gain_factor
            self.pid.i = self.i / external_loop_gain * gain_factor
            self.pid.input = input.signal()
        if offset is not None:
            self.pid.ival = offset
        return

    def _setup_offset(self, offset):
        self.pid.ival = offset

    def _setup(self):
        self._setup_ongoing = True
        if self.assisted_design:
            self.i = self.desired_unity_gain_frequency
            if self.analog_filter_cutoff == 0:
                self.p = 0
            else:
                self.p = self.i / self.analog_filter_cutoff
        else:
            self.desired_unity_gain_frequency = self.i
            if self.p == 0:
                self.analog_filter_cutoff = 0
            else:
                self.analog_filter_cutoff = self.i / self.p
        self._setup_ongoing = False
        if self.current_state == 'sweep':
            self.sweep()
        elif self.current_state == 'unlock':
            self.unlock()
        elif self.current_state == 'lock':
            self.lock()
        self.lockbox._signal_launcher.update_transfer_function.emit([self])

    def tf_freqs(self):
        """
        Frequency values to plot the transfer function. Frequency (abcissa) of
        the tf_curve if tf_type=="curve", else: logspace(0, 6, 20000)
        """
        if self.tf_type == 'curve':
            try:
                c = CurveDB.get(self.tf_curve)
            except:
                self._logger.warning('Cannot load specified transfer function %s', self.tf_curve)
            else:
                return c.data.index

        return np.logspace(0, 6, 2000)

    def transfer_function(self, freqs):
        """
        Returns the design transfer function for the output
        """
        analog_tf = np.ones(len(freqs), dtype=complex)
        if self.tf_type == 'filter':
            analog_tf = Pid._filter_transfer_function(freqs, self.analog_filter_cutoff)
        if self.tf_type == 'curve':
            curve = CurveDB.get(self.tf_curve)
            x = curve.data.index
            y = curve.data.values
            ampl = interpolate.interp1d(x, abs(y))(freqs)
            phase = interpolate.interp1d(x, np.unwrap(np.angle(y)))(freqs)
            analog_tf = ampl * np.exp(complex(0.0, 1.0) * phase)
        result = analog_tf * Pid._transfer_function(freqs, p=self.p, i=self.i, frequency_correction=self.pid._frequency_correction, filter_values=self.additional_filter)
        return result


class PiezoOutput(OutputSignal):
    unit = SelectProperty(default='m/V', options=lambda inst: [ u + '/V' for u in inst.lockbox._output_units ], call_setup=True)