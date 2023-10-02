from typing import Any
from qcodes.instrument import VisaInstrument
from qcodes.parameters import Parameter
from qcodes.validators import Enum, Strings

class KeysightDSOX2014A(VisaInstrument):
    """
    This is the QCoDeS driver for the Keysight_DSOX2014A Oscilloscope.
    """

    def __init__(self, name: str, address: str, channel: int, **kwargs: Any) -> None:
        super().__init__(name, address, terminator="\n", **kwargs)

        idn = self.IDN.get()
        self.model = idn["model"]

        self.add_parameter(
            "voltage",
            get_cmd=f"MEAS:VAV? CHAN{channel}",
            label="Voltage",
            get_parser=float,
            unit="V",
        )
        self.connect_message()

    def reset(self) -> None:
        self.write("*RST")