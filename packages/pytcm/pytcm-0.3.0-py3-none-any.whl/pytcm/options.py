# -*- coding: utf-8 -*-


from dataclasses import dataclass
from typing import Protocol


class Option(Protocol):
    def parse(self) -> str:
        ...


@dataclass
class Flag:
    """A boolean option

    e.g.: --verbose
    """

    abbreviation: str
    value: bool = False

    def parse(self) -> str:
        return self.abbreviation if self.value else ""


@dataclass
class Positional:
    """An simple inline option

    e.g.: example.txt
    """

    value: str = ""

    def parse(self) -> str:
        return self.value


@dataclass
class Implicit:
    """An option separated by a space character

    e.g.: --exclude example.txt
    """

    abbreviation: str
    value: str

    def parse(self) -> str:
        return f"{self.abbreviation} {self.value}"


@dataclass
class Explicit:
    """An option with an equal sign

    e.g.: --exclude=example.txt
    """

    abbreviation: str
    value: str

    def parse(self) -> str:
        return f"{self.abbreviation}={self.value}"
