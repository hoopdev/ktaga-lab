import time

import nidaqmx
import numpy as np
from qcodes.instrument.base import Instrument
from qcodes.validators import Arrays, Bool, Enum, Ints, Numbers


class Magnet(Instrument):
    """
    This is the QCoDeS python driver to control the magnet of
    TOEI in-plane magnetic prober.
    """

    def __init__(
        self,
        name: str,
        daq_address: str,
        v_hall_address: str,
        v_out_address: str,
        read_sample_clock: int = 10000,
        read_sample_num: int = 100,
        time_voltage_sweep: float = 10e-3,
        write_sample_clock: int = 100e3,
        write_array_length: int = 1e3,
        **kwargs,
    ) -> None:
        """
        QCoDeS driver for TOEI in-plane magnetic prober.
        Args:
            name: Name of the instrument.
            time_voltage_sweep: Time to sweep voltage.
                Defaults to 10e-3 s.
        """

        super().__init__(name=name, **kwargs)
        self._V_UNIT = nidaqmx.constants.VoltageUnits.VOLTS
        self._V_IN_TERM_CONF = nidaqmx.constants.TerminalConfiguration.RSE
        self._V_MIN = -10
        self._V_MAX = 10
        self._daq_address = daq_address
        self._v_hall_address = v_hall_address
        self._v_out_address = v_out_address
        self._read_sample_num = read_sample_num
        self._read_sample_clock = read_sample_clock
        self._time_voltage_sweep = time_voltage_sweep
        self._write_sample_clock = write_sample_clock
        self._write_array_length = write_array_length
        self._measured_voltage = 0
        self._output_voltage = 0
        self._measured_field = 0
        self._output_field = 0

        self.add_parameter(
            name="voltage_measured",
            unit="Volts",
            get_cmd=self._get_measured_voltage,
            docstring="Voltage of hall sensor",
            vals=Numbers(min_value=-10, max_value=10),
        )
        self.add_parameter(
            name="field_measured",
            unit="Oe",
            get_cmd=self._get_measured_field,
            docstring="Measured magnetic field of magnet",
            vals=Numbers(min_value=-5000, max_value=5000),
        )
        self.add_parameter(
            name="voltage_output",
            unit="Volts",
            get_cmd=self._get_output_voltage,
            set_cmd=self._set_output_voltage,
            docstring="Output voltage of magnet",
            vals=Numbers(min_value=-10, max_value=10),
        )
        self.add_parameter(
            name="field_output",
            unit="Oe",
            get_cmd=self._get_output_field,
            set_cmd=self._set_output_field,
            docstring="Output magnetic field of magnet",
            vals=Numbers(min_value=-5000, max_value=5000),
        )

        self.connect_message()

    def H2V(self, H: float) -> float:
        """Convert target magnetic field to output voltage
        input: magnetic field (Oe)
        output: voltage (V)
        """
        V = (
            -0.01268
            + 0.00281 * H
            + 3.02608e-10 * H**2
            - 1.5036e-11 * H**3
            - 1.66895e-16 * H**4
            + 3.15376e-18 * H**5
        )
        return V

    def V2H(self, V: float) -> float:
        """Convert hall voltage to magnetic field
        input: hall voltage (V)
        output: magnetic field (Oe)
        """
        H = (
            -0.05665
            + 260.16273 * V
            - 2.1979e-5 * V**2
            + 0.01858 * V**3
            + 1.97225e-4 * V**4
            - 2.33726e-4 * V**5
        )
        return H

    def _get_measured_voltage(self) -> float:
        """Return measured hall voltage"""
        task = nidaqmx.Task()
        task.ai_channels.add_ai_voltage_chan(
            f"{self._daq_address}/{self._v_hall_address}",
            min_val=self._V_MIN,
            max_val=self._V_MAX,
            terminal_config=self._V_IN_TERM_CONF,
            units=self._V_UNIT,
        )
        task.timing.cfg_samp_clk_timing(self._read_sample_clock)
        data = task.read(number_of_samples_per_channel=self._read_sample_num)
        task.wait_until_done()
        task.stop()
        task.close()
        V = np.mean(data)
        self._measured_voltage = V
        return V

    def _get_measured_field(self) -> float:
        """Return measured magnetic field using hall sensor"""
        V = self._get_measured_voltage()
        H = self.V2H(V)
        self._measured_field = H
        return H

    def _set_output_voltage(self, voltage: float) -> None:
        """Set output voltage of magnet"""
        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan(
            f"{self._daq_address}/{self._v_out_address}",
            min_val=self._V_MIN,
            max_val=self._V_MAX,
        )
        task.timing.cfg_samp_clk_timing(self._write_sample_clock)
        v_out = np.linspace(
            self._output_voltage, voltage, self._write_array_length
        )
        task.write(v_out, auto_start=True)
        task.wait_until_done()
        task.stop()
        task.close()
        self._output_voltage = voltage
        time.sleep(0.1)
        return

    def _get_output_voltage(self) -> float:
        """Get output voltage of magnet"""
        return self._output_voltage

    def _set_output_field(self, target_field: float) -> None:
        """Set output magnetic field of magnet"""
        target_voltage = self.H2V(target_field)
        self._set_output_voltage(target_voltage)
        self._output_field = target_field
        return

    def _get_output_field(self) -> float:
        """Get output magnetic field of magnet"""
        return self._output_field
