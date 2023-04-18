from typing import Any

from qcodes.instrument import VisaInstrument
from qcodes.parameters import Parameter
from qcodes.validators import Enum, Strings


class Keysight34420A(VisaInstrument):
    """
    This is the QCoDeS driver for the Keysight_34420A NanovoltMeter.
    """

    def __init__(self, name: str, address: str, **kwargs: Any) -> None:
        super().__init__(name, address, terminator="\n", **kwargs)

        idn = self.IDN.get()
        self.model = idn["model"]

        NPLC_list = {
            "34420A": [0.02, 0.2, 1, 2, 10, 20, 100, 200],
        }[self.model]

        self._resolution_factor = {
            "34420A": [1e-4, 1e-5, 3e-6, 2.2e-6, 1e-6, 8e-7, 3e-7, 2.2e-7],
        }[self.model]

        self.resolution = Parameter(
            "resolution",
            instrument=self,
            get_cmd="VOLT:DC:RES?",
            get_parser=float,
            set_cmd=self._set_resolution,
            label="Resolution",
            unit="V",
        )
        """Resolution """

        self.add_parameter(
            "volt",
            get_cmd="READ?",
            label="Voltage",
            get_parser=float,
            unit="V",
        )

        self.add_parameter(
            "fetch",
            get_cmd="FETCH?",
            label="Voltage",
            get_parser=float,
            unit="V",
            snapshot_get=False,
            docstring=(
                "Reads the data you asked for, i.e. "
                "after an `init_measurement()` you can "
                "read the data with fetch.\n"
                "Do not call this when you did not ask "
                "for data in the first place!"
            ),
        )

        self.add_parameter(
            "NPLC",
            get_cmd="VOLT:NPLC?",
            get_parser=float,
            set_cmd=self._set_nplc,
            vals=Enum(*NPLC_list),
            label="Integration time",
            unit="NPLC",
        )

        self.add_parameter("terminals", get_cmd="ROUT:TERM?")

        self.add_parameter(
            "range_auto",
            get_cmd="VOLT:RANG:AUTO?",
            set_cmd="VOLT:RANG:AUTO {:d}",
            val_mapping={"on": 1, "off": 0},
        )

        self.add_parameter(
            "range",
            get_cmd="SENS:VOLT:DC:RANG?",
            get_parser=float,
            set_cmd="SENS:VOLT:DC:RANG {:f}",
            vals=Enum(0.1, 1.0, 10.0, 100.0, 1000.0),
        )

        self.connect_message()

    def _set_nplc(self, value: float) -> None:
        self.write(f"VOLT:NPLC {value:f}")
        # resolution settings change with NPLC
        self.resolution.get()

    def _set_resolution(self, value: float) -> None:
        rang = self.range.get()
        # convert both value*range and the resolution factors
        # to strings with few digits, so we avoid floating point
        # rounding errors.
        res_fac_strs = [f"{v * rang:.1e}" for v in self._resolution_factor]
        if f"{value:.1e}" not in res_fac_strs:
            raise ValueError(
                "Resolution setting {:.1e} ({} at range {}) "
                "does not exist. "
                "Possible values are {}".format(
                    value, value, rang, res_fac_strs
                )
            )
        self.write(f"VOLT:DC:RES {value:.1e}")
        # NPLC settings change with resolution
        self.NPLC.get()

    def _set_range(self, value: float) -> None:
        self.write(f"SENS:VOLT:DC:RANG {value:f}")
        # resolution settings change with range
        self.resolution.get()

    def clear_errors(self) -> None:
        while True:
            err = self.ask("SYST:ERR?")
            if "No error" in err:
                return
            print(err)

    def init_measurement(self) -> None:
        self.write("INIT")

    def reset(self) -> None:
        self.write("*RST")
