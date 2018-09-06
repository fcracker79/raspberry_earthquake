import math
import os
from pprint import pprint

import earthquake
from earthquake import steps_converter_factory, reader
from earthquake.steps_converter import StepItem

_STEP_TIME = 0.1
_SCALE_FACTOR = 1 / 50.0
_RADIUS = 0.02
_FILENAME = os.path.join(os.path.dirname(earthquake.__file__), '..', 'data/SISMA A-(1).Txt')

result = steps_converter_factory.create_for_step_motor(
    _STEP_TIME, _SCALE_FACTOR, _RADIUS
).convert_to_steps(
    reader.TabbedFileEarthquakeReader(_FILENAME, 2).read()
)
result = map(lambda d: StepItem(d.value / math.pi * 180), result)
result = list(result)
print('Points:', len(result))
pprint(result)

