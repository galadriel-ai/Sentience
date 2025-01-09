from typing import List

from sentience.agent_framework.agents.logging_utils import get_agent_logger
from sentience.agent_framework.agents.models import AgentConfig
from sentience.agent_framework.agents.models import Memory
from sentience.agent_framework.agents.clients.database import DatabaseClient


logger = get_agent_logger()


class AgentState:
    memories: List[Memory]
    database: DatabaseClient
    # TODO: knowledge_base: KnowledgeBase


class GaladrielAgent:

    def __init__(
        # For now can put in what ever you want
        agent_config: AgentConfig,
        # Things consumed by python - OpenAI, Galadriel API, Database etc...
        # This allows the community to add all sorts of clients useful for Agent
        # TODO: not sure yet
        # clients: List[Client],
        # Things consumed by LLMs - calculator, web search etc..
        # This is allows the community to develop all sorts of tools and easy
        # for developers to create new ones
        # TODO: not sure yet
        # tools: List[Tool],
    ):
        pass

    # Does not take any input parameters so it can be run from anywhere
    async def run():
        # No abstractions, implement your while loop completely without any
        # building blocks
        pass

    # Gathers all the data that the Agent is using and exporting it as one class
    async def export_state() -> AgentState:
        pass

    # Restores the Agent state from one class.
    # Should be called before calling run()
    async def load_state(agent_state: AgentState):
        pass

    async def upload_state(self):
        state = self.export_state()
        upload(state)

    async def restore_state(self):
        state = download()
        self.load_state(state)
