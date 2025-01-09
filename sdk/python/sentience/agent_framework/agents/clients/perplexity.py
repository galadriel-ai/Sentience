import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp

from sentience.agent_framework.agents.logging_utils import get_agent_logger

logger = get_agent_logger()


@dataclass
class PerplexitySources:
    content: str
    sources: str


class PerplexityClient:
    api_key: str

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search_topic(self, topic: str) -> Optional[PerplexitySources]:
        logger.info(f"Using perplexity API with search query: {topic}")
        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {"role": "system", "content": "Be precise and concise."},
                {"role": "user", "content": topic},
            ],
            "max_tokens": 10000,
            "temperature": 0.2,
            "top_p": 0.9,
            "search_domain_filter": ["perplexity.ai"],
            "return_images": False,
            "return_related_questions": False,
            "search_recency_filter": "month",
            "top_k": 0,
            "stream": False,
            "presence_penalty": 0,
            "frequency_penalty": 1,
        }

        timeout = 60
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url, headers=headers, json=payload, timeout=timeout  # type: ignore
                ) as response:
                    response.raise_for_status()

                    response_json = await response.json()
                    content = response_json["choices"][0]["message"]["content"]
                    sources = "\n".join(
                        [
                            f"[{index + 1}] {url}"
                            for index, url in enumerate(
                                response_json.get("citations", [])
                            )
                        ]
                    )

                    result = PerplexitySources(
                        content=content,
                        sources=sources,
                    )
                    logger.info("API call successful")
                    return result
        except asyncio.TimeoutError:
            logger.error("The request timed out.")
        except aiohttp.ClientError as e:
            logger.error(f"An error occurred: {e}")
        return None
