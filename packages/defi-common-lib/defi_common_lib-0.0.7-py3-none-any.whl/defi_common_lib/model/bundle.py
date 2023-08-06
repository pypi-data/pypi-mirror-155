from dataclasses import dataclass
import datetime
from typing import List

from defi_common_lib.model.dataset import Dataset


@dataclass
class Bundle:
    id: int
    user: str
    created_at: datetime
    updated_at: datetime
    status: str
    datasets: List[Dataset]

    def __init__(self,
                 id: int,
                 user: str,
                 created_at: datetime,
                 updated_at: datetime,
                 status: str,
                 price: float,
                 datasets: List[Dataset]
                 ) -> None:

        self.id = id
        self.user = user
        self.created_at = created_at
        self.updated_at = updated_at
        self.status = status
        self.datasets = datasets
        self.price = price
