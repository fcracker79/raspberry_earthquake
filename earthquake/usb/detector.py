import os
import threading
import time
import typing
import psutil
import pyttsx3
import pyudev
import retrying

from earthquake import eq_runner, reader, steps_converter_factory


class StopException(Exception):
    pass


class USBDetector:
    _SLEEP_TIME = 0.1
    _STEP_TIME = 0.1
    _SCALE_FACTOR = 1 / 50.0
    _RADIUS = 0.02
    _PIN = 7

    def __init__(self):
        self._current_thread = None  # type: typing.Optional[threading.Thread]
        self._stopped = True
        self._speech_engine = pyttsx3.init()

    def _tick_function(self):
        if self._stopped:
            raise StopException

    @retrying.retry(wait_fixed=2000)
    def _get_new_initial_partitions(self, old_partitions: typing.List[str]) -> typing.List[str]:
        initial_partitions = [p.mountpoint for p in psutil.disk_partitions() if p.fstype == 'vfat']
        if not initial_partitions:
            raise Exception
        return initial_partitions

    def start_engine(self, filenames: typing.List[str]):
        self._play_text('Playing {}'.format([os.path.basename(x) for x in filenames]))
        self.stop_engine()

        def _f():
            from earthquake.engines import gpio
            for filename in filenames:
                if self._stopped:
                    break
                self._play_text('Playing file {}'.format(filename))
                eq_runner.run(
                    reader.TabbedFileEarthquakeReader(filename, 2),
                    steps_converter_factory.create_for_step_motor(
                        self._STEP_TIME, self._SCALE_FACTOR, self._RADIUS
                    ),
                    gpio.GPIOEngine(self._PIN),
                    self._SLEEP_TIME,
                    self._tick_function
                )
        self._current_thread = threading.Thread(target=_f)
        self._current_thread.daemon = True
        self._stopped = False
        self._current_thread.start()

    def stop_engine(self):
        self._play_text('Stopping engine')
        self._stopped = True
        if not self._current_thread:
            return

        while self._current_thread.is_alive():
            print('Waiting for thread to die')
            time.sleep(2)
        self._current_thread.join()

    def _play_text(self, text: str):
        print(text)
        self._speech_engine.say(text)
        self._speech_engine.runAndWait()

    def __call__(self, *args, **kwargs):
        self._play_text('Hi there!')
        initial_partitions = []
        while not initial_partitions:
            self.context = pyudev.Context()
            self.monitor = pyudev.Monitor.from_netlink(self.context)
            self.monitor.filter_by(subsystem='usb')
            # this is module level logger, can be ignored
            self.monitor.start()
            all_devices = set()
            for device in iter(self.monitor.poll, None):
                if device.action not in ('bind', 'unbind'):
                    continue
                add = device.action == 'bind'
                while device.parent:
                    device = device.parent
                if add and device.sys_path not in all_devices:
                    self.stop_engine()
                    self._play_text('New device detected')
                    all_devices.add(device.sys_path)
                    initial_partitions = self._get_new_initial_partitions(initial_partitions)
                elif not add and device.sys_path in all_devices:
                    self.stop_engine()
                    self._play_text('Device removed')
                    all_devices.remove(device.sys_path)
                    initial_partitions = [p.mountpoint for p in psutil.disk_partitions() if p.fstype == 'vfat']
                else:
                    print('Nothing to do')
                    continue
                print('Mountpoints', initial_partitions)
                if initial_partitions:
                    self._play_text('Reading files from USB')
                    files = [os.path.join(initial_partitions[0], x) for x in os.listdir(initial_partitions[0])]
                    for i, file in enumerate(files):
                        self._play_text('File {}: {}'.format(i + 1, os.path.basename(file)))
                    self.start_engine(files)

d = USBDetector()
# d.on_created.append(lambda x: print('+ {}: {}'.format(type(x), x)))
# d.on_deleted.append(lambda x: print('- {}: {}'.format(type(x), x)))
d()