import json
import os
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

import aiofiles

from sentience.agent_framework.agents.logging_utils import get_agent_logger
from sentience.agent_framework.agents.models import Memory

logger = get_agent_logger()

MEMORIES_FILE = "memories.json"


class DatabaseClient:
    memories_file_path: str

    def __init__(
        self,
        data_dir: str = "data",
    ):
        os.makedirs(data_dir, exist_ok=True)
        self.memories_file_path = os.path.join(data_dir, MEMORIES_FILE)

        if not os.path.exists(self.memories_file_path):
            with open(self.memories_file_path, "w", encoding="utf-8") as f:
                f.write(json.dumps([]))

    async def _get_memories(self) -> List[Memory]:
        try:
            content = await _read_json_list(self.memories_file_path)
            return [Memory.from_dict(c) for c in content]
        except Exception:
            return []

    async def get_tweets(self) -> List[Memory]:
        try:
            memories = await self._get_memories()
            return [m for m in memories if m.type == "tweet"]
        except Exception:
            logger.error("Failed to get tweets", exc_info=True)
            return []

    async def get_latest_tweet(self) -> Optional[Memory]:
        tweets = await self.get_tweets()
        if not tweets:
            return None
        return tweets[-1]

    async def add_memory(self, memory: Memory) -> None:
        try:
            memories = await self._get_memories()
            memories.append(memory)
            memories_dict = [m.to_dict() for m in memories]
            await _write_json(self.memories_file_path, memories_dict)
        except Exception:
            logger.error("Failed to get memories", exc_info=True)
            return None


async def _read_json_list(file_path: str) -> List[Dict]:
    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        content = await f.read()
        return json.loads(content)


async def _write_json(file_path: str, content: Union[List, Dict]) -> None:
    async with aiofiles.open(file_path, "w", encoding="utf-8") as f:
        await f.write(json.dumps(content, indent=4))
