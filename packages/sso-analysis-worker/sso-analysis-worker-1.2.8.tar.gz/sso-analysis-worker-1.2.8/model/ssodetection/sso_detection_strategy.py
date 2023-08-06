from enum import Enum


class SSODetectionStrategy(Enum):
    MANUAL = 1,
    ELEMENT_SEARCH = 2,
    IMAGE_ANALYSIS = 3,
    NONE = 4
