from dataclasses import dataclass


@dataclass
class SQLiteVersion:
    version: str
    date: str
    release_log: str
    url: str
