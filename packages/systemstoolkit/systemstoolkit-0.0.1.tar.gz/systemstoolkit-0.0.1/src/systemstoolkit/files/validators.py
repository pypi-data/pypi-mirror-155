import numpy as np
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple


class InvalidDataError(Exception):
    pass


class DataValidator(ABC):
    def validate(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        raise NotImplementedError


class NoValidator(DataValidator):
    def validate(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        return time, data


@dataclass
class DataShapeValidator(DataValidator):
    ncols: Optional[int] = None
    nrows: Optional[int] = None

    def validate(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        nrows, ncols = data.shape
        if self.ncols is not None and self.ncols != ncols:
            raise InvalidDataError

        if self.nrows is not None and self.nrows != nrows:
            raise InvalidDataError

        return time, data


@dataclass
class QuaternionValidator(DataValidator):
    tolerance: float = 1e-5
    shape_validator: DataShapeValidator = DataShapeValidator(ncols=4)

    def validate(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        self.shape_validator.validate(time, data)

        rss = np.abs(np.sqrt(np.sum(data ** 2, axis=1)) - 1)
        print(rss)
        idx = rss < self.tolerance

        if np.sum(idx) == 0:
            raise InvalidDataError

        return time[idx], data[idx, :]


@dataclass
class AngleValidator(DataValidator):
    max_angle: float = 360
    shape_validator: DataShapeValidator = DataShapeValidator(ncols=3)

    def validate(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        self.shape_validator.validate(time, data)

        max = np.abs(np.max(data, axis=1))
        idx = max < self.max_angle

        if np.sum(idx) == 0:
            raise InvalidDataError

        return time[idx], data[idx, :]
