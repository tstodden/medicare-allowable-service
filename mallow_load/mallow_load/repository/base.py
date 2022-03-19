import csv
from abc import ABCMeta, abstractmethod
from typing import Any, TextIO


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get(self, key: Any) -> Any:
        raise NotImplementedError()

    @abstractmethod
    def _add_row_to_repository(self, row: dict[str, str]) -> None:
        raise NotImplementedError()

    def add_csv_file(self, file: TextIO) -> None:
        reader = csv.DictReader(file)
        for row in reader:
            self._add_row_to_repository(row)
