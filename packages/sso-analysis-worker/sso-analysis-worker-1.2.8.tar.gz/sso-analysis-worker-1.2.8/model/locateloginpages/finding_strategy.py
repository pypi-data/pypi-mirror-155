from enum import Enum


class FindingStrategy(Enum):
    GOOD_LUCK_AUTOMATIC = 1,
    GOOD_LUCK_EXTRA_STEPS = 2,
    MANUAL = 3,
    NONE = 4
