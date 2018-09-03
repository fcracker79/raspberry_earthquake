import unittest
from unittest import mock

from earthquake.eq_item import EarthquakeItem
from earthquake.steps_converter import StepperStepsConverter, StepItem, ScalingDelegateStepsConverter, StepsConverter, \
    DelegateDeltaStepsConverter


class TestStepperStepsConverter(unittest.TestCase):
    def test(self):
        fixture = [
            EarthquakeItem(9.8, 10),
            EarthquakeItem(9.8, 20),
            EarthquakeItem(9.8, 30)
        ]
        sut = StepperStepsConverter(2)
        result = sut.convert_to_steps(fixture)
        count = 0
        for i, r in enumerate(result):
            self.assertAlmostEqual(
                0.5 * 9.8 * (i * 2 + 2) ** 2,
                r.value, delta=0.00001, msg='Error in {}'.format(i)
            )
            count += 1
        self.assertEqual(15, count)


class TestScalingDelegateStepsConverter(unittest.TestCase):
    def test(self):
        fixture = [
            StepItem(x) for x in range(10)
        ]
        delegate = mock.create_autospec(StepsConverter)
        delegate.convert_to_steps.return_value = fixture
        sut = ScalingDelegateStepsConverter(delegate, 123.0)
        result = sut.convert_to_steps(mock.ANY)
        count = 0
        for i, r in enumerate(result):
            self.assertEqual(123.0 * i, r.value)
            count += 1
        self.assertEqual(len(fixture), count)


class TestDelegateDeltaStepsConverter(unittest.TestCase):
    def test(self):
        fixture = [
            StepItem(x) for x in range(10)
        ]
        delegate = mock.create_autospec(StepsConverter)
        delegate.convert_to_steps.return_value = fixture
        sut = DelegateDeltaStepsConverter(delegate)
        result = sut.convert_to_steps(mock.ANY)
        count = 0
        for r in result:
            self.assertEqual(1, r.value)
            count += 1
        self.assertEqual(len(fixture) - 1, count)
