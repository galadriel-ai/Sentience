from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from sentience.agent_framework.agents.models import Memory
from sentience.agent_framework.agents.prompts import get_search_query
from sentience.agent_framework.agents.prompts.get_search_query import SearchQuery


async def test_success():
    agent = MagicMock()
    agent.search_queries = {
        "key": ["value"],
    }
    db = AsyncMock()
    db.get_tweets.return_value = []

    result = await get_search_query.execute(agent, db)
    assert result == SearchQuery(topic="key", query="value")


async def test_excludes_used_topic():
    agent = MagicMock()
    agent.search_queries = {
        "key1": ["value1"],
        "key2": ["value2"],
    }
    db = AsyncMock()
    db.get_tweets.return_value = [
        Memory(
            id="mock_id",
            type="tweet",
            text="mock_text",
            topics=["key1"],
            timestamp=123,
            search_topic="key1",
            quoted_tweet_id=None,
            quoted_tweet_username=None,
        )
    ]

    result = await get_search_query.execute(agent, db)
    assert result == SearchQuery(topic="key2", query="value2")


async def test_no_topics_to_exclude():
    agent = MagicMock()
    agent.search_queries = {
        "key1": ["value1"],
    }
    db = AsyncMock()
    db.get_tweets.return_value = [
        Memory(
            id="mock_id",
            type="tweet",
            text="mock_text",
            topics=[],
            timestamp=123,
            search_topic=None,
            quoted_tweet_id=None,
            quoted_tweet_username=None,
        )
    ]

    result = await get_search_query.execute(agent, db)
    assert result == SearchQuery(topic="key1", query="value1")
