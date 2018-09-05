import abc
import re
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
    def read_from_line(self, idx: int, line: str) -> typing.Optional[EarthquakeItem]:
        pass

    def read(self) -> typing.Iterator[EarthquakeItem]:
        with open(self._filename, 'rt') as f:
            for i, l in enumerate(f.readlines()):
                cur_item = self.read_from_line(i, l)
                if cur_item:
                    yield cur_item


class TabbedFileEarthquakeReader(FileBasedEarthquakeReader):
    _STR_PATTERN = '([^\t ]+)[\t ]+([^\t ]+)'
    _PATTERN = re.compile(_STR_PATTERN)

    def __init__(self, filename: str, header_lines: int):
        super(TabbedFileEarthquakeReader, self).__init__(filename)
        self._header_lines = header_lines

    def read_from_line(self, idx: int, line: str) -> typing.Optional[EarthquakeItem]:
        if idx < self._header_lines:
            return None
        matcher = re.fullmatch(self._PATTERN, line)
        if not matcher:
            return None
        return EarthquakeItem(float(matcher.group(2)), float(matcher.group(1)))
