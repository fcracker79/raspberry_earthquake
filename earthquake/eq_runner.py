import time

from earthquake.engines import Engine
from earthquake.reader import EarthquakeReader
from earthquake.steps_converter import StepsConverter


def run(reader: EarthquakeReader, steps_converter: StepsConverter, engine: Engine, sleep_time: float):
    engine.init_engine()
    time.sleep(1)
    for step in steps_converter.convert_to_steps(reader.read()):
        engine.move(step)
        time.sleep(sleep_time)
    time.sleep(1)
    engine.park_engine()
