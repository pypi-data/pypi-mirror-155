from dataclasses import dataclass


@dataclass
class Dataset:
    id: int
    key: str
    source: str

    def __init__(self, id: int, key: str, source: str, file_name: str) -> None:
        self.id = id
        self.key = key
        self.source = source
        self.file_name = file_name

