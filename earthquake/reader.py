import abc
import typing

from earthquake.eq_item import EarthquakeItem


class EarthquakeReader(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def read(self) -> typing.Iterator[EarthquakeItem]:
        pass


class FileBasedEarthquakeReader(EarthquakeReader, metaclass=abc.ABCMeta):
    def __init__(self, filename: str):
        self._filename = filename

    @abc.abstractmethod
    def read_from_line(self, idx: int, line: str) -> EarthquakeItem:
        pass

    def read(self) -> typing.Iterator[EarthquakeItem]:
        with open(self._filename, 'rt') as f:
            for i, l in f.readline():
                cur_item = self.read_from_line(i, l)
                if cur_item:
                    yield cur_item


class TabbedFileEarthquakeReader(FileBasedEarthquakeReader):
    def __init__(self, filename: str, header_lines: int):
        super(TabbedFileEarthquakeReader, self).__init__(filename)
        self._header_lines = header_lines

    def read_from_line(self, idx: int, line: str) -> EarthquakeItem:
        if idx < self._header_lines:
            return None
        return EarthquakeItem(*map(float, line.split('\t')))
