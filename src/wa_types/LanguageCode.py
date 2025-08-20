from enum import Enum

class LanguageCode(Enum):
    EN = "en"
    RU = "ru"

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"{self.__class__.__name__}.{self.name}"
