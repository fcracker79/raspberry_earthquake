import abc
import typing


EarthquakeCallback = typing.NewType('EarthquakeCallback', typing.Callable[[], None])


class EarthquakeController(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def set_on_shutdown_pressed(self, fun: EarthquakeCallback):
        pass

    @abc.abstractmethod
    def set_on_backward_pressed(self, fun: EarthquakeCallback):
        pass

    @abc.abstractmethod
    def set_on_forward_pressed(self, fun: EarthquakeCallback):
        pass

    @abc.abstractmethod
    def set_on_pause_pressed(self, fun: EarthquakeCallback):
        pass

    @abc.abstractmethod
    def start(self):
        pass
