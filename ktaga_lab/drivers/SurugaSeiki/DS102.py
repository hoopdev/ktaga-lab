import time

import serial
from qcodes.instrument.base import Instrument
from qcodes.instrument.parameter import Parameter
from qcodes.validators import Arrays, Bool, Enum, Floats, Ints, Numbers


class Axis(Parameter):
    """Sets the axis for parameter"""

    def __init__(
        self, name: str, instrument: "MotorDriver", axis: int, **kwargs
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)
        self.axis = axis

    def get_raw(self) -> int:
        return self.axis

    def set_raw(self, value: int) -> None:
        self.axis = value


class CWSoftLimitEnable(Parameter):
    """Sets the CW soft limit enable"""

    def __init__(
        self, name: str, instrument: "MotorDriver", axis: int, **kwargs
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)
        self.axis = axis

    def get_raw(self) -> int:
        return self.instrument.ask(f":CWSoftLimitEnable_{self.axis}")

    def set_raw(self, value: int) -> None:
        self.instrument.write(f":CWSoftLimitEnable_{self.axis} {value}")


class CWSoftLimitPoint(Parameter):
    """Sets the CW soft limit point"""

    def __init__(
        self, name: str, instrument: "MotorDriver", axis: int, **kwargs
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)
        self.axis = axis

    def get_raw(self) -> int:
        return self.instrument.ask(f":CWSoftLimitPoint_{self.axis}")

    def set_raw(self, value: int) -> None:
        self.instrument.write(f":CWSoftLimitPoint_{self.axis} {value}")


class CCWSoftLimitEnable(Parameter):
    """Sets the CCW soft limit enable"""

    def __init__(
        self, name: str, instrument: "MotorDriver", axis: int, **kwargs
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)
        self.axis = axis

    def get_raw(self) -> int:
        return self.instrument.ask(f":CCWSoftLimitEnable_{self.axis}")

    def set_raw(self, value: int) -> None:
        self.instrument.write(f":CCWSoftLimitEnable_{self.axis} {value}")


class CCWSoftLimitPoint(Parameter):
    """
    Sets the CCW soft limit point.
    """

    def __init__(
        self, name: str, instrument: "MotorDriver", axis: int, **kwargs
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)
        self.axis = axis

    def get_raw(self) -> int:
        return self.instrument.ask(f":CCWSoftLimitPoint_{self.axis}")

    def set_raw(self, value: int) -> None:
        self.instrument.write(f":CCWSoftLimitPoint_{self.axis} {value}")


class DriverDivision(Parameter):
    """Sets the driver division for microstepping or full step operation.
    Args:
        name: Name of the parameter.
        instrument: The instrument object.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument)

    def set_raw(self, value: int):
        """Sets the driver division."""
        if not 0 <= value <= 15:
            raise ValueError("Driver division must be between 0 and 15.")
        self.instrument.write(f":DRDIV_{value}")

    def get_raw(self) -> int:
        """Gets the current driver division."""
        response = self.instrument.ask(":DRDIV?")
        return int(response)


class Data(Parameter):
    """Sets the data channel for multi-data channel systems.
    Args:
        name: Name of the parameter.
        instrument: The instrument object.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument)

    def set_raw(self, value: int):
        """Sets the data channel."""
        if value not in [1, 2]:
            raise ValueError("Data channel must be 1 or 2.")
        self.instrument.write(f":DATA_{value}")

    def get_raw(self) -> int:
        """Gets the current data channel."""
        response = self.instrument.ask(":DATA?")
        return int(response)


class HomePosition(Parameter):
    """Sets the home position value for the motor.
    Args:
        name: Name of the parameter.
        instrument: The instrument object.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument)

    def set_raw(self, value: float):
        """Sets the home position value."""
        if not -99999999 <= value <= 99999999:
            raise ValueError(
                "Home position must be between -99999999 and 99999999."
            )
        self.instrument.write(f":HOMEP_{value}")

    def get_raw(self) -> float:
        """Gets the current home position value."""
        response = self.instrument.ask(":HOMEP?")
        return float(response)


class Position(Parameter):
    """Sets the current position of the motor.
    Args:
        name: Name of the parameter.
        instrument: The instrument object.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument)

    def set_raw(self, value: float):
        """Sets the current position."""
        if not -99999999 <= value <= 99999999:
            raise ValueError(
                "Position must be between -99999999 and 99999999."
            )
        self.instrument.write(f":POS_{value}")

    def get_raw(self) -> float:
        """Gets the current position."""
        response = self.instrument.ask(":POS?")
        return float(response)


class Pulse(Parameter):
    """Class for setting the constant pulse movement amount.
    Args:
        name (str): The name of the parameter.
        instrument (MotorDriver): The instance of the parent MotorDriver instrument.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument=instrument, **kwargs)

    def get_raw(self):
        """Get the current pulse value."""
        return int(self.instrument.ask("PULS?"))

    def set_raw(self, value):
        """Set the pulse value."""
        self.instrument.write(f"PULS {int(value)}")


class PulseA(Parameter):
    """Class for setting the absolute position of the motor.
    Args:
        name (str): The name of the parameter.
        instrument (MotorDriver): The instance of the parent MotorDriver instrument.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument=instrument, **kwargs)

    def get_raw(self):
        """Get the current absolute position of the motor."""
        return int(self.instrument.ask("PULSA?"))

    def set_raw(self, value):
        """Set the absolute position of the motor."""
        self.instrument.write(f"PULSA {int(value)}")


class SelectSpeed(Parameter):
    """Class for setting the speed table of the motor.
    Args:
        name (str): The name of the parameter.
        instrument (MotorDriver): The instance of the parent MotorDriver instrument.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument=instrument, **kwargs)

    def get_raw(self):
        """Get the current speed table."""
        return int(self.instrument.ask("SELSP?"))

    def set_raw(self, value):
        """Set the speed table."""
        self.instrument.write(f"SELSP {int(value)}")


class StandardResolution(Parameter):
    """Class for setting the pulse distance for full step.
    Args:
        name (str): The name of the parameter.
        instrument (MotorDriver): The instance of the parent MotorDriver instrument.
        **kwargs: Keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: "MotorDriver", **kwargs):
        super().__init__(name, instrument=instrument, **kwargs)

    def get_raw(self):
        """Get the current standard resolution."""
        return int(self.instrument.ask("STANDARD?"))

    def set_raw(self, value):
        """Set the standard resolution."""
        self.instrument.write(f"STANDARD {int(value)}")


class Unit(Parameter):
    """Displayed unit setting.
    Args:
        name (str): Name of the parameter.
        instrument (Instrument): Parent instrument object that this parameter belongs to.
        **kwargs: Additional keyword arguments to be passed to the Parameter constructor.
    """

    def __init__(self, name: str, instrument: Instrument, **kwargs) -> None:
        super().__init__(name, instrument=instrument, **kwargs)

    def set_raw(self, unit: str) -> None:
        """Sets displayed unit.
        Args:
            unit (str): Displayed unit.
                "PULSe(PULS)": Pulse unit.
                "UM": Micro meter unit.
                "MM": Milli meter unit.
                "DEG": Degree unit.
                "MRAD": Milli radian unit.
        """
        self.instrument.write(f"UNI {unit}")

    def get_raw(self) -> str:
        """Returns displayed unit."""
        unit = self.instrument.query("UNI?")
        return unit.strip()


class MotorDriver(Instrument):
    """
    DS102 Driver for controlling a motor
    """

    def __init__(
        self,
        name: str,
        com_port: str,
        baudrate: int = 9600,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)
        self.metadata.update(
            {
                "com_port": com_port,
                "baudrate": baudrate,
            }
        )
        try:
            self.ser = serial.Serial()
            self.ser.port = com_port
            self.ser.baudrate = baudrate
            self.ser.bytesize = serial.EIGHTBITS
            self.ser.parity = serial.PARITY_NONE
            self.ser.stopbits = serial.STOPBITS_ONE
            self.ser.timeout = 0.1
            self.ser.xonxoff = False
            self.ser.rtscts = False
            self.ser.dsrdtr = False
            self.ser.writeTimeout = 0

            self.ser.open()
            time.sleep(1)
        except Exception as e:
            print("Error opening serial port")
            print(e)
            exit()

        if self.ser.isOpen():
            try:
                self.ser.flushInput()
                self.ser.flushOutput()
            except Exception as e1:
                print("Error Communicating...: " + str(e1))
        else:
            print("Cannot open serial port ")

        self.add_parameter(
            name="axis",
            parameter_class=Axis,
            label="Motor axis",
            unit="",
            values=[
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "X",
                "Y",
                "Z",
                "U",
                "V",
                "W",
                "ALL",
            ],
        )

        self.add_parameter(
            name="cw_soft_limit_enable",
            parameter_class=CWSoftLimitEnable,
            label="CW soft limit enable",
            unit="",
            values=["0", "1"],
        )

        self.add_parameter(
            name="cw_soft_limit_point",
            parameter_class=CWSoftLimitPoint,
            label="CW soft limit point",
            unit="",
            vals=Ints(-99999999, 99999999),
        )

        self.add_parameter(
            name="ccw_soft_limit_enable",
            parameter_class=CCWSoftLimitEnable,
            label="CCW soft limit enable",
            unit="",
            values=["0", "1"],
        )

        self.add_parameter(
            name="ccw_soft_limit_point",
            parameter_class=CCWSoftLimitPoint,
            label="CCW soft limit point",
            unit="",
            vals=Ints(-99999999, 99999999),
        )
        self.add_parameter(
            name="driver_division",
            parameter_class=DriverDivision,
            label="Driver division",
            unit="",
            vals=Ints(0, 15),
        )
        self.add_parameter(
            name="data",
            parameter_class=Data,
            label="Data",
            unit="",
            vals=Ints(1, 2),
        )
        self.add_parameter(
            name="home_position",
            parameter_class=HomePosition,
            label="Home position",
            unit="",
            vals=Ints(-99999999, 99999999),
        )
        self.add_parameter(
            name="pulse",
            parameter_class=Pulse,
            label="Pulse",
            unit="",
            vals=Ints(0, 99999999),
        )
        self.add_parameter(
            name="pulse_absolute",
            parameter_class=PulseA,
            label="Pulse absolute",
            unit="",
            vals=Ints(-99999999, 99999999),
        )
        self.add_parameter(
            name="select_speed",
            parameter_class=SelectSpeed,
            Label="Select speed",
            unit="",
            vals=Ints(0, 9),
        )
        self.add_parameter(
            name="standard_resolution",
            parameter_class=StandardResolution,
            label="Standard resolution",
            unit="",
            vals=Ints(0, 99999999),
        )
        self.add_parameter(
            name="unit",
            parameter_class=Unit,
            label="Unit",
            unit="",
            values=["PULSe", "UM", "MM", "DEG", "MRAD"],
        )
        self.connect_message()

    def get_idn(self):
        return {
            "vendor": "Motor",
            "model": "",
            "serial": None,
            "firmware": None,
        }

    def write(self, cmd: str) -> None:
        self.ser.write((cmd + "\r").encode())
        time.sleep(0.3)

    def rst(self) -> None:
        """
        Reset all parameters to default
        """
        self.write("*RST")
        time.sleep(5)

    def go(self, go_option: int) -> None:
        """
        Controls the motor to drive in the specified direction.

        Args:
            option (int): The option to drive the motor in. Valid values are:
                0 (or CW) for clockwise direction.
                1 (or CCW) for counterclockwise direction.
                2 (or OriGin(ORG)) for returning to the origin point.
                3 (or HOME) for moving to the home position.
                4 (or ABS) for absolute position.
                5 (or CWJ) for clockwise jogging.
                6 (or CCWJ) for counterclockwise jogging.
        """

        if go_option not in {0, 1, 2, 3, 4, 5, 6}:
            raise ValueError("Invalid direction")
        # Send command to control the motor in the specified direction
        command = f":GO_{go_option}"
        self.write(command)

    def go_absolute(self, position: int) -> None:
        """
        Commands the motor to drive to absolute position.

        Args:
            position (int): The absolute position to drive the motor to.
        """

        command = f":GOABS_{position}"
        self.write(command)

    def stop(self, stop_mode: int) -> None:
        """
        Stops the motor.

        Args:
            stop_mode (int): The mode to stop the motor in. Valid values are:
                0 (or E) for emergency stop.
                1 (or R) for reduction stop.
        """

        if stop_mode not in {0, 1}:
            raise ValueError("Invalid stop mode")
        # Send command to stop the motor in the specified mode
        command = f":STOP_{stop_mode}"
        self.write(command)

    def stop_all_axis(self, stop_mode: int) -> None:
        """
        Stops the motor.

        Args:
            stop_mode (int): The mode to stop the motor in. Valid values are:
                0 (or E) for emergency stop.
                1 (or R) for reduction stop.
        """

        if stop_mode not in {0, 1}:
            raise ValueError("Invalid stop mode")
        # Send command to stop the motor in the specified mode
        command = f"STOP_{stop_mode}"
        self.write(command)
