import abc
import typing

from earthquake.eq_item import EarthquakeItem


StepItem = typing.NamedTuple('StepItem', (('value', float), ) )


class StepsConverter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def convert_to_steps(self, eq_items: typing.Iterator[EarthquakeItem]) -> typing.Iterator[StepItem]:
        pass


class ScalingDelegateStepsConverter(StepsConverter):
    def __init__(self, delegate: StepsConverter, scale_factor: float):
        self._delegate = delegate
        self._scale_factor = scale_factor

    def _scale_step_item(self, s: StepItem) -> StepItem:
        return StepItem(s.value * self._scale_factor)

    def convert_to_steps(self, eq_items: typing.Iterator[EarthquakeItem]) -> typing.Iterator[StepItem]:
        yield from map(self._scale_step_item, self._delegate.convert_to_steps(eq_items))


class StepperStepsConverter(StepsConverter):
    def __init__(self, step_time: float):
        self._step_time = step_time

    def convert_to_steps(self, eq_items: typing.Iterator[EarthquakeItem]) -> typing.Iterator[StepItem]:
        cur_speed = cur_position = 0.0
        previous_item = None
        for item in eq_items:
            time_delta = item.time_slice - (previous_item.time_slice if previous_item else 0)
            if not time_delta:
                continue
            if time_delta < self._step_time:
                continue
            steps = int(time_delta / self._step_time)
            for step in range(steps):
                cur_position += \
                    0.5 * item.acceleration * self._step_time * self._step_time + \
                    cur_speed * self._step_time
                cur_speed += item.acceleration * self._step_time
                yield StepItem(cur_position)
            previous_item = item


class DelegateAngularStepsConverter(StepsConverter):
    def __init__(self, delegate: StepsConverter, radius: float):
        self._delegate = delegate
        self._radius = radius

    def _convert_step_item(self, step_item: StepItem) -> StepItem:
        return StepItem(step_item.value / self._radius)

    def convert_to_steps(self, eq_items: typing.Iterator[EarthquakeItem]) -> typing.Iterator[StepItem]:
        yield from map(self._convert_step_item, self._delegate.convert_to_steps(eq_items))


class DelegateDeltaStepsConverter(StepsConverter):
    def __init__(self, delegate: StepsConverter):
        self._delegate = delegate

    def convert_to_steps(self, eq_items: typing.Iterator[EarthquakeItem]) -> typing.Iterator[StepItem]:
        previous_item = None
        for step_item in self._delegate.convert_to_steps(eq_items):
            if not previous_item:
                previous_item = step_item
                continue
            yield StepItem(step_item.value - previous_item.value)
            previous_item = step_item
