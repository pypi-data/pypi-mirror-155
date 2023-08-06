from enum import Enum, auto


class SyncType(Enum):
    COUNT = auto(),
    LOGS = auto(),
    NONE = auto(),

    def __str__(self):
        return self.name

    @staticmethod
    def from_string(s):
        try:
            return SyncType[s]
        except KeyError:
            raise ValueError()