import abc

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
