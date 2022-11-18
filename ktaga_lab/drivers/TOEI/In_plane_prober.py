import time

import nidaqmx
import numpy as np
from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import Parameter
from qcodes.validators import Arrays, Bool, Enum, Ints, Numbers

V_UNIT = nidaqmx.constants.VoltageUnits.VOLTS
V_IN_TERM_CONF = nidaqmx.constants.TerminalConfiguration.RSE
V_MIN = -10
V_MAX = 10


class OutputField(Parameter):
    """Output magnetic field by writing voltage value to daq.
    Args:
        name: Name of parameter.
        dev_name: DAQ device name (e.g. 'Dev1').
        v_out_address: AO address.
        time_voltage_sweep: DAQ AO time to sweep voltage.
        write_sample_clock: DAQ AO sampling clock.
        write_array_length: DAQ AO sampling length.
        kwargs: Keyword arguments to be passed to ArrayParameter constructor.
    """

    def __init__(
        self,
        name: str,
        dev_name: str,
        v_out_address: str,
        time_voltage_sweep: float,
        write_sample_clock: int,
        write_array_length: int,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        self.dev_name = dev_name
        self.v_out_address = v_out_address
        self.time_voltage_sweep = time_voltage_sweep
        self.write_sample_clock = write_sample_clock
        self.write_array_length = write_array_length
        self._voltage = 0
        self._field = 0

        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan(
            f"{self.dev_name}/{self.v_out_address}",
            min_val=V_MIN,
            max_val=V_MAX,
        )
        task.timing.cfg_samp_clk_timing(self.write_sample_clock)
        v_out = np.zeros(int(self.write_array_length))
        task.write(v_out, auto_start=True)
        task.wait_until_done()
        task.stop()
        task.close()

    def set_raw(self, field: float) -> None:
        """Set output voltage of magnet"""
        voltage = self.H2V(field)
        task = nidaqmx.Task()
        task.ao_channels.add_ao_voltage_chan(
            f"{self.dev_name}/{self.v_out_address}",
            min_val=V_MIN,
            max_val=V_MAX,
        )
        task.timing.cfg_samp_clk_timing(self.write_sample_clock)
        v_out = np.linspace(
            self._voltage, voltage, int(self.write_array_length)
        )
        print(v_out)
        task.write(v_out, auto_start=True)
        task.wait_until_done()
        task.stop()
        task.close()
        self._voltage = voltage
        self._field = field
        time.sleep(0.1)
        print(self._voltage)
        print(self._field)
        return

    def get_raw(self):
        """Returns last voltage written to outputs."""
        return self._field

    def H2V(self, H: float) -> float:
        """Convert target magnetic field to output voltage.
        input: magnetic field (mT)
        output: voltage (V)
        """
        H = H * 10  # convert from mT to Oe
        V = (
            -0.01268
            + 0.00281 * H
            + 3.02608e-10 * H**2
            - 1.5036e-11 * H**3
            - 1.66895e-16 * H**4
            + 3.15376e-18 * H**5
        )
        return V


class MeasuredField(Parameter):
    """Measured magnetic field by reading voltage value to daq
    Args:
        name: Name of parameter.
        dev_name: DAQ device name (e.g. 'Dev1').
        v_hall_address: DAQ AI ch. of hall voltage.
        read_sample_num: DAQ AI sampling number.
        read_sample_clock: DAQ AI sampling clock.
        kwargs: Keyword arguments to be passed to ArrayParameter constructor.
    """

    def __init__(
        self,
        name: str,
        dev_name: str,
        v_hall_address: str,
        read_sample_num: int,
        read_sample_clock: int,
        **kwargs,
    ) -> None:
        super().__init__(name, **kwargs)
        self.dev_name = dev_name
        self.v_hall_address = v_hall_address
        self.read_sample_num = read_sample_num
        self.read_sample_clock = read_sample_clock
        self._voltage = np.nan
        self._field = np.nan

    def get_raw(self):
        """Returns measured magnetic field from hall voltage"""
        task = nidaqmx.Task()
        task.ai_channels.add_ai_voltage_chan(
            f"{self.dev_name}/{self.v_hall_address}",
            min_val=V_MIN,
            max_val=V_MAX,
            terminal_config=V_IN_TERM_CONF,
            units=V_UNIT,
        )
        task.timing.cfg_samp_clk_timing(self.read_sample_clock)
        data = task.read(number_of_samples_per_channel=self.read_sample_num)
        task.wait_until_done()
        task.stop()
        task.close()
        V = np.mean(data)
        self._voltage = V
        self._field = self.V2H(self._voltage)
        return self._field

    def V2H(self, V: float) -> float:
        """Convert hall voltage to magnetic field
        input: hall voltage (V)
        output: magnetic field (mT)
        """
        H = (
            -0.05665
            + 260.16273 * V
            - 2.1979e-5 * V**2
            + 0.01858 * V**3
            + 1.97225e-4 * V**4
            - 2.33726e-4 * V**5
        )
        H = H / 10  # convert from Oe to mT
        return H


class Magnet(Instrument):
    """
    This is the QCoDeS python driver to control the magnet of
    TOEI in-plane magnetic prober.
    """

    def __init__(
        self,
        name: str,
        dev_name: str,
        v_hall_address: str,
        v_out_address: str,
        read_sample_num: int = 100,
        read_sample_clock: int = 10000,
        time_voltage_sweep: float = 10e-3,
        write_sample_clock: int = 100e3,
        write_array_length: int = 1e3,
        **kwargs,
    ) -> None:
        """
        QCoDeS driver for TOEI in-plane magnetic prober.
        Args:
            name: Name of the instrument.
            dev_name: DAQ device name (e.g. 'Dev1').
            v_hall_address: DAQ AI ch. of hall voltage.
            v_out_address: DAQ AO ch. of magnet voltage.
            read_sample_num: DAQ AI sampling number.
            read_sample_clock: DAQ AI sampling clock.
            time_voltage_sweep: DAQ AO time to sweep voltage.
            write_sample_clock: DAQ AO sampling clock.
            write_array_length: DAQ AO sampling length.
        """

        super().__init__(name=name, **kwargs)
        self.metadata.update(
            {
                "dev_name": dev_name,
                "v_hall_address": v_hall_address,
                "v_out_address": v_out_address,
                "read_sample_num": read_sample_num,
                "read_sample_clock": read_sample_clock,
                "time_voltage_sweep": time_voltage_sweep,
                "write_sample_clock": write_sample_clock,
                "write_array_length": write_array_length,
            }
        )

        self.add_parameter(
            name="measured_field",
            dev_name=dev_name,
            v_hall_address=v_hall_address,
            read_sample_num=read_sample_num,
            read_sample_clock=read_sample_clock,
            parameter_class=MeasuredField,
            label="Magnetic field",
            unit="mT",
        )
        self.add_parameter(
            name="output_field",
            dev_name=dev_name,
            v_out_address=v_out_address,
            time_voltage_sweep=time_voltage_sweep,
            write_sample_clock=write_sample_clock,
            write_array_length=write_array_length,
            parameter_class=OutputField,
            label="Magnetic field",
            unit="mT",
        )

        self.connect_message()

    def get_idn(self):
        return {
            "vendor": "TOEI",
            "model": "In-plane prober",
            "serial": None,
            "firmware": None,
        }
