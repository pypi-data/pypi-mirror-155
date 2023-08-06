import numpy as np
from enum import Enum, auto
from dataclasses import dataclass, asdict
from typing import Optional, Union

from systemstoolkit.utils import stk_datetime
from systemstoolkit.typing import DateTimeLike, ArrayLike
from systemstoolkit.units.time import (
    TimeUnit,
    EpSecTimeUnit,
    EpMinTimeUnit,
    EpHrTimeUnit,
    EpDayTimeUnit,
    # EpYearTimeUnit,
    YYYYDDDTimeUnit,
    YYYYMMDDTimeUnit,
    ISOYMDTimeUnit,
)


KEYWORD_WIDTH = 30


class Keyword:
    @property
    def keyword(self) -> str:
        return self.__class__.__name__

    def __str__(self) -> str:
        return f'{str(self.keyword).ljust(KEYWORD_WIDTH)} {self.value}'


class CompoundKeyword(Keyword):
    def __str__(self) -> str:
        # Iterate through the dataclass fields
        # returning formatted keywords that are not None
        keywords = [getattr(self, key) for key in asdict(self)]
        return '\n'.join([str(key) for key in keywords if key is not None])


class KeywordEnum(Enum):
    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower() == name.lower():
                return member
    
    def _generate_next_value_(name, start, count, last_values):
        return name

    def __str__(self) -> str: # pragma: no cover
        return f'{str(self.keyword).ljust(KEYWORD_WIDTH)} {self.name}'


class MessageLevel(Keyword, KeywordEnum):
    Errors = auto()
    Warnings = auto()
    Verbose = auto()


class CentralBody(Keyword, KeywordEnum):
    Earth = auto()
    Moon = auto()


class CoordinateAxes(Keyword, KeywordEnum):
    ICRF = auto()
    J2000 = auto()
    Inertial = auto()
    Fixed = auto()
    TrueOfDate = auto()
    MeanOfDate = auto()
    TEMEOfDate = auto()
    B1950 = auto()
    MeanOfEpoch = auto()
    TrueOfEpoch = auto()
    TEMEOfEpoch = auto()
    AlignmentAtEpoch = auto()


class AttitudeDeviations(Keyword, KeywordEnum):
    Rapid = auto()
    Mild = auto()


class InterpolationMethod(Keyword, KeywordEnum):
    Lagrange = auto()
    Hermite = auto()


@dataclass
class InterpolationOrder(Keyword):
    value: int = 1


@dataclass
class Epoch(Keyword):
    value: DateTimeLike

    def __post_init__(self):
        self.value = np.datetime64(self.value)

    def __str__(self) -> str:
        return f'{str(self.keyword).ljust(KEYWORD_WIDTH)} {stk_datetime(self.value)}'


class ScenarioEpoch(Epoch):
    pass


class CoordinateAxesEpoch(Epoch):
    pass


@dataclass
class Coordinate(CompoundKeyword):
    axes: CoordinateAxes
    epoch: Optional[CoordinateAxesEpoch] = None

    def __post_init__(self):
        if 'epoch' in self.axes.value.lower():
            if self.epoch is None:
                raise ValueError(f'CoordinateAxes "{self.axes.value}" requires a CoordinateAxesEpoch')
        else:
            if self.epoch is not None:
                raise ValueError(f'CoordinateAxes "{self.axes.value}" does not support CoordinateAxesEpoch')


@dataclass
class Interpolation(CompoundKeyword):
    method: InterpolationMethod
    order: Optional[InterpolationOrder]


@dataclass
class NumberOfAttitudePoints(Keyword):
    value: int = None


@dataclass
class BlockingFactor(Keyword):
    value: int = None


class InitialAttitude(Keyword):
    pass


# class KeywordObjectEnum(KeywordEnum):

class TimeFormat(Keyword, KeywordEnum):
    EpSec = EpSecTimeUnit
    EpMin = EpMinTimeUnit
    EpHour = EpHrTimeUnit
    EpDays = EpDayTimeUnit
    # EpYear = EpYearTimeUnit
    YYYYDDD = YYYYDDDTimeUnit
    YYYYMMDD = YYYYMMDDTimeUnit
    ISOYMD = ISOYMDTimeUnit

    @classmethod
    def _missing_(cls, name):
        for member in cls:
            if member.name.lower() == name.replace('-', '').lower():
                return member

    def convert(self, time: ArrayLike, epoch=None) -> ArrayLike:
        time_fmt = self.value(epoch)
        return time_fmt.convert(time)

    def __str__(self) -> str: # pragma: no cover
        return f'{str(self.keyword).ljust(KEYWORD_WIDTH)} {self.name}'


class TrendingControl(Keyword):
    pass
