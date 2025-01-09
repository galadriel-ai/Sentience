import random
from dataclasses import dataclass

from sentience.agent_framework.agents.clients.database import DatabaseClient
from sentience.agent_framework.agents.logging_utils import get_agent_logger
from sentience.agent_framework.agents.models import AgentConfig

MAX_SEARCH_TOPICS_COUNT = 7

logger = get_agent_logger()


@dataclass
class SearchQuery:
    topic: str
    query: str


async def execute(agent: AgentConfig, database: DatabaseClient) -> SearchQuery:
    all_search_topics = list(agent.search_queries.keys())
    tweets = await database.get_tweets()
    used_search_topics = []
    for tweet in reversed(tweets):
        if search_topic := tweet.search_topic:
            used_search_topics.append(search_topic)
        if len(used_search_topics) >= MAX_SEARCH_TOPICS_COUNT:
            break
    filtered_search_topics = [
        t for t in all_search_topics if t not in used_search_topics
    ]
    try:
        topic = random.choice(filtered_search_topics)
        return SearchQuery(
            topic=topic,
            query=random.choice(agent.search_queries.get(topic, [])),
        )
    except Exception:
        logger.error("Error choosing search query", exc_info=True)
        return SearchQuery(
            topic="",
            query="",
        )
