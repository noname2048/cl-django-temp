from dataclasses import dataclass
from datetime import timedelta


@dataclass
class DurationValidatorInput:
    duration: timedelta
