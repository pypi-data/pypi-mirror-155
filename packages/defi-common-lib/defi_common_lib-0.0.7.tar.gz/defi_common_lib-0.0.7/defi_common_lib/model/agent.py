from dataclasses import dataclass


@dataclass
class Agent:
    id: int
    category: str
    subcategory: str
    description: str

    def __init__(self, id: int, category: str, subcategory: str) -> None:
        self.id = id
        self.category = category
        self.subcategory = subcategory
