"""
Mount & Blade Warband game configs
Here's a place for settings specific for installed Mount & Blade Warband game
"""

from os import path
from pathlib import Path

from wa_types import LanguageCode


# Loading language code from game settings
with open(path.join(Path.home(), ".mbwarband/language.txt")) as file:
    code_str = file.readline().rstrip()
try:
    language_code = LanguageCode(code_str)
except ValueError:
    language_code = LanguageCode.EN
