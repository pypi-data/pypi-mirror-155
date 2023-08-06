from dataclasses import dataclass
from datetime import datetime
from defi_common_lib.db.database_service import DatabaseService
from defi_common_lib.db.querys import UPDATE_AGENT_STATE


@dataclass
class AgentState:
    agent_id: int
    protocol_id: int
    protocol_name: str
    protocol_chain: str
    protocol_version: str
    periodidity: str
    last_updated: str
    last_entry: str
    price: float
    db: DatabaseService

    def __init__(self,
                 agent_id: int,
                 protocol_id: int,
                 protocol_name: str,
                 protocol_chain: str,
                 protocol_version: str,
                 periodidity: str,
                 last_updated: str,
                 last_entry: str,
                 price: float,
                 db: DatabaseService) -> None:

        self.agent_id = agent_id
        self.protocol_id = protocol_id
        self.protocol_name = protocol_name
        self.protocol_chain = protocol_chain
        self.protocol_version = protocol_version
        self.periodidity = periodidity
        self.last_updated = last_updated
        self.last_entry = last_entry
        self.price = price
        self.db = db

    def update_last_state(self, date: datetime, last_entry: str):
        updated = self.db.execute(
            sql=UPDATE_AGENT_STATE,
            data=(date, last_entry, self.agent_id, self.protocol_id)
        )

        return updated
