from enum import Enum

class SampleMatch(Enum):
    # exact match
    MATCH = "match"
    # partial match
    DOUBT = "doubt"
    # no matches
    FAIL = "fail"

    def __bool__(self):
        return self is SampleMatch.MATCH
