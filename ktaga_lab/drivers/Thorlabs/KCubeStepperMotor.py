import sys
import time
import clr
from System import Decimal, String
from qcodes.instrument.parameter import Parameter
from qcodes.instrument.base import Instrument

sys.path.append(r"C:\Program Files\Thorlabs\Kinesis")

# add .net reference and import so python can see .net
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("Thorlabs.MotionControl.KCube.StepperMotorCLI")
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from Thorlabs.MotionControl.KCube.StepperMotorCLI import KCubeStepper

class KCubeStepperMotor(Instrument):
    """
    Thorlabs Kinesis KCube Stepper Motor
    """
    def __init__(
        self,
        name: str,
        serial: str,
        min_velocity: float = 0.0,
        max_velocity: float = 0.5,
        acceleration: float = 0.2,
        **kwargs,
    ) -> None:
        super().__init__(name=name, **kwargs)

        self.min_velocity = min_velocity
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.serial = serial

        self.metadata.update(
            {
                "serial": serial,
                "acceleration": acceleration,
                "min_velocity": min_velocity,
                "max_velocity": max_velocity,
            }
        )

        # Motor initialization
        DeviceManagerCLI.BuildDeviceList()
        self.device = KCubeStepper.CreateKCubeStepper(serial)
        self.device.Connect(serial)
        self.device.WaitForSettingsInitialized(5000)
        self.motorSettings = self.device.LoadMotorConfiguration(serial)
        self.device.StartPolling(250)
        self.device.EnableDevice()
        self.deviceInfo = self.device.GetDeviceInfo()

        # Configure velocity parameters
        self.motor_config()

        # Create Position parameter
        self.add_parameter(
            name="position",
            parameter_class=Position,
            label="Motor position",
            unit="mm",
        )

    def motor_config(self):
        velocity_params = self.device.GetVelocityParams()
        velocity_params.Acceleration = Decimal(self.acceleration)
        velocity_params.MinVelocity = Decimal(self.min_velocity)
        velocity_params.MaxVelocity = Decimal(self.max_velocity)
        self.device.SetVelocityParams(velocity_params)

    def disconnect(self):
        self.device.StopPolling()
        self.device.ShutDown()

    def get_position(self):
        return float(str(self.device.Position))

    def go_home(self):
        self.device.Home(60000)
        time.sleep(0.1)
        return

    def move_position(self, position):
        self.device.MoveTo(Decimal(float(position)), 60000)
        time.sleep(0.1)
        return

    def get_idn(self):
        return {
            "vendor": "Thorlabs",
            "model": "KST201",
            "serial": self.serial,
            "firmware": None,
        }

class Position(Parameter):
    """
    Parameter class for the motor position
    """
    def __init__(
        self,
        name: str,
        instrument: KCubeStepperMotor,
        **kwargs,
    ) -> None:
        super().__init__(name, instrument=instrument, **kwargs)

    def set_raw(self, position: float) -> None:
        """Sets the motor position"""
        self.instrument.move_position(position)

    def get_raw(self) -> float:
        """Returns the motor position"""
        return self.instrument.get_position()