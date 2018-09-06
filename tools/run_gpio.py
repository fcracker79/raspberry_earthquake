import os
import sys
import earthquake
from earthquake import steps_converter_factory, reader, eq_runner
from earthquake.engines import gpio

_SLEEP_TIME = 0.1
_STEP_TIME = 0.1
_SCALE_FACTOR = 1 / 50.0
_RADIUS = 0.003
_PIN = 7

_ROOT = os.path.join(os.path.dirname(earthquake.__file__), '..', 'data')
_FILENAMES = [os.path.join(_ROOT, x) for x in os.listdir(_ROOT)]

print(_FILENAMES)
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(
            'Usage: {} step\nwith step:\n{}'.format(
                sys.argv[0],
                '\n'.join('\t{} - {}'.format(i, f) for i, f in enumerate(_FILENAMES)))
        )
        exit(1)

    eq_runner.run(
        reader.TabbedFileEarthquakeReader(_FILENAMES[int(sys.argv[-1])], 2),
        steps_converter_factory.create_for_step_motor(
            _STEP_TIME, _SCALE_FACTOR, _RADIUS
        ),
        gpio.GPIOEngine(_PIN),
        _SLEEP_TIME
    )
