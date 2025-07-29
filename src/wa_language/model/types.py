from enum import Enum


class LordPersonality(Enum):
    MARTIAL = "martial"
    BADTEMPERED = "badtempered"
    PITILESS = "pitiless"
    CUNNING = "cunning"
    SADISTIC = "sadistic"
    GOODNATURED = "goodnatured"
    UPSTANDING = "upstanding"


class LangModelError(Exception):
    pass
