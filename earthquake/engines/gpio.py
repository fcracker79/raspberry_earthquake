import math

# noinspection PyUnresolvedReferences
import RPi.GPIO as GPIO

from earthquake.engines import Engine
from earthquake.steps_converter import StepItem


class GPIOEngine(Engine):
    def __init__(
            self, pin: int,
            start_duty_cycle: int=2,
            end_duty_cycle: int=11,
            _180_degrees_value: float=math.pi):
        self._pin = pin
        self._pwm = None
        self._start_duty_cycle = start_duty_cycle
        self._end_duty_cycle = end_duty_cycle
        self._180_degrees_value = _180_degrees_value

    def init_engine(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._pin, GPIO.OUT)
        self._pwm = GPIO.PWM(self._pin, 50)
        self._pwm.start(0)

    def park_engine(self):
        self.move(StepItem(0.0))
        self._pwm and self._pwm.stop()
        GPIO.cleanup()
        self._started = False

    def move(self, step_item: StepItem) -> None:
        duty_cycle = float(step_item.value) / self._180_degrees_value * \
                     (self._end_duty_cycle - self._start_duty_cycle) / 2 \
                     + self._start_duty_cycle \
                     + (self._end_duty_cycle - self._start_duty_cycle) / 2
        print('Dino', step_item.value, self._180_degrees_value,
              self._end_duty_cycle, duty_cycle)
        self._pwm.ChangeDutyCycle(duty_cycle)
