import enum
import typing

from inputs import get_gamepad

from earthquake.controllers import EarthquakeController, EarthquakeCallback


class Button(enum.Enum):
    THUMB = 'BTN_THUMB'
    THUMB2 = 'BTN_THUMB2'
    TOP = 'BTN_TOP'
    TRIGGER = 'BTN_TRIGGER'
    ABS_X = 'ABS_X'
    ABS_Y = 'ABS_Y'


class GamepadController:
    _BTNS = {
        x.value for x in Button
    }

    def __init__(self):
        self._btn_statuses = dict()
        self._listeners = {
            b: [] for b in Button
        }

    def add_listener(self, button: Button, fun: typing.Callable[[int, int], None]):
        self._listeners[button].append(fun)

    def start(self):
        while True:
            for event in get_gamepad():
                # print('Event type', event.ev_type, 'Code', event.code, 'State', event.state)
                if event.code in self._BTNS:
                    self._set_button_state(Button(event.code), event.state)
            # print('Fine')

    def _set_button_state(self, button: Button, state):
        old_value = self._btn_statuses.get(button)
        if old_value != state:
            self._btn_statuses[button] = state
            for f in self._listeners[button]:
                f(old_value, state)


class GamepadEarthquakeController(EarthquakeController):
    def __init__(self, controller: GamepadController):
        self._controller = controller

    def set_on_shutdown_pressed(self, fun: EarthquakeCallback):
        def _f(old_value, new_value):
            if old_value == 1 and new_value == 0:
                fun()
        self._controller.add_listener(Button.THUMB, _f)

    def set_on_back_pressed(self, fun: EarthquakeCallback):
        def _f(old_value, new_value):
            if old_value == 0 and new_value == 127:
                fun()
        self._controller.add_listener(Button.ABS_X, _f)

    def set_on_forward_pressed(self, fun: EarthquakeCallback):
        def _f(old_value, new_value):
            if old_value == 255 and new_value == 127:
                fun()
        self._controller.add_listener(Button.ABS_X, _f)

    def set_on_pause_pressed(self, fun: EarthquakeCallback):
        def _f(old_value, new_value):
            if old_value == 1 and new_value == 0:
                fun()
        self._controller.add_listener(Button.THUMB2, _f)

    def start(self):
        self._controller.start()


# g = GamepadEarthquakeController(GamepadController())
# g.set_on_back_pressed(lambda: print('Back'))
# g.set_on_forward_pressed(lambda: print('Forward'))
# g.set_on_pause_pressed(lambda: print('Pause'))
# g.set_on_shutdown_pressed(lambda: print('Shutdown'))
# g.start()
