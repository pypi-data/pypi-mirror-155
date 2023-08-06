import numpy as np
from enum import auto
from typing import Tuple

from systemstoolkit.files.keywords import KeywordEnum
from systemstoolkit.files.validators import (
    DataValidator,
    QuaternionValidator,
    AngleValidator,
    NoValidator,
)


class DataFileFormat(KeywordEnum):
    def validate_data(self, time: np.ndarray, data: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        return self.validator.validate(time, data)


class AttitudeFileFormat(DataFileFormat):
    # Quaternion-based formats
    Quaternions = auto()
    QuatScalarFirst = auto()
    QuatAngVels = auto()
    AngVels = auto()

    # Euler-based Formats
    EulerAngles = auto()
    EulerAngleRates = auto()
    EulerAnglesAndRates = auto()

    # YPR-based formats
    YPRAngles = auto()
    YPRAngleRates = auto()
    YPRAnglesAndRates = auto()

    # DCM-based formats
    DCM = auto()
    DCMAngVels = auto()

    # Vector-based formats
    ECFVector = auto()
    ECIVector = auto()

    def __str__(self) -> str:
        return f'AttitudeTime{self.name}'

    @property
    def validator(self) -> DataValidator:
        if self.name in ['Quaternions', 'QuatScalarFirst']:
            return QuaternionValidator()
        elif self.name in ['EulerAngles', 'YPRAngles']:
            return AngleValidator()
        else:
            return NoValidator()
