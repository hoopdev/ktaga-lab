import warnings
from typing import TYPE_CHECKING, Any

import numpy as np
import qcodes.validators as vals
from qcodes.instrument import VisaInstrument, VisaInstrumentKWArgs
from qcodes.parameters import Parameter, create_on_off_val_mapping

if TYPE_CHECKING:
    from typing_extensions import Unpack


class AgilentE8251A(VisaInstrument):
    """This is the QCoDeS driver for the Agilent E8251A signal generator.
    This driver will most likely work for multiple Agilent sources.
    This driver does not contain all commands available for the E8251A but
    only the ones most commonly used.
    """

    default_terminator = "\n"

    def __init__(
        self,
        name: str,
        address: str,
        step_attenuator: bool | None = None,
        **kwargs: "Unpack[VisaInstrumentKWArgs]",
    ) -> None:
        super().__init__(name, address, **kwargs)

        if step_attenuator is not None:
            warnings.warn(
                "step_attenuator argument to E8251A is deprecated "
                "and has no effect. It will be removed in the "
                "future.",
            )

        # assign min and max frequencies
        self._min_freq: float = 250e3
        self._max_freq: float = 20e9

        # assign min and max powers
        self._min_power: float = -135
        self._max_power: float = 25

        self.frequency: Parameter = self.add_parameter(
            name="frequency",
            label="Frequency",
            unit="Hz",
            get_cmd="FREQ:CW?",
            set_cmd="FREQ:CW" + " {:.4f}",
            get_parser=float,
            set_parser=float,
            vals=vals.Numbers(self._min_freq, self._max_freq),
        )
        """Parameter frequency"""

        self.phase: Parameter = self.add_parameter(
            name="phase",
            label="Phase",
            unit="deg",
            get_cmd="PHASE?",
            set_cmd="PHASE" + " {:.8f}",
            get_parser=self.rad_to_deg,
            set_parser=self.deg_to_rad,
            vals=vals.Numbers(-180, 180),
        )
        """Parameter phase"""

        self.power: Parameter = self.add_parameter(
            name="power",
            label="Power",
            unit="dBm",
            get_cmd="POW:AMPL?",
            set_cmd="POW:AMPL" + " {:.4f}",
            get_parser=float,
            set_parser=float,
            vals=vals.Numbers(self._min_power, self._max_power),
        )
        """Parameter power"""

        self.output_enabled: Parameter = self.add_parameter(
            "output_enabled",
            get_cmd=":OUTP?",
            set_cmd="OUTP {}",
            val_mapping=create_on_off_val_mapping(on_val="1", off_val="0"),
        )
        """Parameter output_enabled"""

        self.connect_message()

    def on(self) -> None:
        self.output_enabled.set("on")

    def off(self) -> None:
        self.output_enabled.set("off")

    # functions to convert between rad and deg
    @staticmethod
    def deg_to_rad(
        angle_deg: float | str | np.floating | np.integer,
    ) -> "np.floating[Any]":
        return np.deg2rad(float(angle_deg))

    @staticmethod
    def rad_to_deg(
        angle_rad: float | str | np.floating | np.integer,
    ) -> "np.floating[Any]":
        return np.rad2deg(float(angle_rad))
