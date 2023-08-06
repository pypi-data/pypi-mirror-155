from defi_common_lib.db.database_service import DatabaseService
from defi_common_lib.db.querys import SELECT_AGENT
from defi_common_lib.model.agent import Agent


class AgentSelection:

    def __init__(self, agent_id: int, db: DatabaseService):
        self.agent_id = agent_id
        self.db = db

    def get_agent(self) -> Agent:
        agent_data = self.db.get_all_rows(sql=SELECT_AGENT, data=(self.agent_id))

        if len(agent_data) > 0:
            agent = Agent(
                id=agent_data[0]['agent_id'],
                category=agent_data[0]['category'],
                subcategory=agent_data[0]['subcategory'],
            )
        else:
            raise Exception(f'Agent not found for id: {self.agent_id}')

        return agent