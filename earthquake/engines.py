import abc
import math

from earthquake.steps_converter import StepItem


class Engine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def init_engine(self):
        pass

    @abc.abstractmethod
    def park_engine(self):
        pass

    @abc.abstractmethod
    def move(self, step_item: StepItem) -> None:
        pass


class ServoMotorEngine(Engine):
    def __init__(self, servo_max_deg: float=180):
        self._servo_max_deg = servo_max_deg

    @classmethod
    def _set_property_to_pwm(cls, prop: str, value):
        with open("/sys/class/rpi-pwm/pwm0/" + prop, 'w') as f:
            f.write(value)
            f.close()

    @classmethod
    def _set_servo_angle(cls, angle):
        cls._set_property_to_pwm('servo', str(angle))

    def init_engine(self):
        self._set_property_to_pwm('delayed', '0')
        self._set_property_to_pwm('mode', 'servo')
        self._set_property_to_pwm('servo_max', float(self._servo_max_deg))
        self._set_property_to_pwm('active', '1')

    def park_engine(self):
        self.move(StepItem(0.0))

    def move(self, step_item: StepItem) -> None:
        self._set_servo_angle(step_item.value / math.pi * 180)
