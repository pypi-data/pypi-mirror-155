from typing import List

from defi_common_lib.model.agent_state import AgentState
from defi_common_lib.model.agent import Agent
from defi_common_lib.db.database_service import DatabaseService
from defi_common_lib.db.querys import SELECT_AGENT_STATE


class AgentSates:

    def __init__(self, agent: Agent, db: DatabaseService):
        self.agent = agent
        self.db = db

    def get_state(self) -> List[AgentState]:
        agent_state_data = self.db.get_all_rows(
            sql=SELECT_AGENT_STATE, data=(self.agent.id)
        )

        states = []

        for state in agent_state_data:
            state_to_update = AgentState(
                agent_id=state['agent_id'],
                protocol_id=state['protocol_id'],
                protocol_name=state['name'],
                protocol_version=state['version'],
                protocol_chain=state['chain'],
                periodidity=state['periodicity'],
                last_updated=state['last_updated'],
                last_entry=state['last_entry'],
                price=state['price'],
                db=self.db,
            )
            states.append(state_to_update)

        return states