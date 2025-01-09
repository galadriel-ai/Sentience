import os
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from requests_oauthlib import OAuth1Session

from sentience.agent_framework.agents.logging_utils import get_agent_logger

logger = get_agent_logger()


@dataclass
class TwitterCredentials:
    consumer_api_key: str
    consumer_api_secret: str
    access_token: str
    access_token_secret: str


@dataclass
class SearchResult:
    id: str
    username: str
    text: str
    retweet_count: int
    reply_count: int
    like_count: int
    quote_count: int
    bookmark_count: int
    impression_count: int
    # Is this needed?
    referenced_tweets: List[Dict]
    attachments: Optional[Dict]


class TwitterConnectionError(Exception):
    """Base exception for Twitter connection errors"""


class TwitterAPIError(TwitterConnectionError):
    """Raised when Twitter API requests fail"""


# TODO: Should not be hardcoded
# pylint: disable=C0301:
SEARCH_QUERY = "(-is:retweet -is:reply -is:quote) (from:aixbt_agent OR from:iruletheworldmo OR from:VitalikButerin OR from:lexfridman OR from:SpaceX OR from:sama OR from:OpenAI OR from:xai OR from:balajis from:karpathy)"


class TwitterClient:
    oauth_session: OAuth1Session

    def __init__(self, _credentials: TwitterCredentials):
        # Might want to look into Oauth2Session, has higher limits, but can we POST tweets with it?
        # https://developer.x.com/en/docs/x-api/rate-limits
        self.oauth_session = OAuth1Session(
            _credentials.consumer_api_key,
            client_secret=_credentials.consumer_api_secret,
            resource_owner_key=_credentials.access_token,
            resource_owner_secret=_credentials.access_token_secret,
        )

    async def post_tweet(self, message: str) -> Optional[Dict]:
        if os.getenv("DRY_RUN"):
            logger.info(f"Would have posted tweet: {message}")
            return {"data": {"id": "dry_run"}}
        response = await self._make_request("POST", "tweets", json={"text": message})
        logger.info(f"Tweet posted successfully: {message}")
        return response

    async def search(self) -> List[SearchResult]:
        try:
            response = await self._make_request(
                "GET",
                "tweets/search/recent",
                params={
                    "query": SEARCH_QUERY,
                    "sort_order": "relevancy",
                    "tweet.fields": "public_metrics,text,author_id,referenced_tweets,attachments",
                    "expansions": "author_id",
                    "user.fields": "name,username",
                    "max_results": 20,
                },
            )
            # import json
            # with open("search3.json", "w", encoding="utf-8") as f:
            #     f.write(json.dumps(response))
            #
            # import json
            # with open("search3.json", "r", encoding="utf-8") as f:
            #     response = json.loads(f.read())

            formatted_results: List[SearchResult] = []
            for result in response.get("data", []):
                public_metrics = result.get("public_metrics", {})
                matching_users = [
                    user
                    for user in response["includes"]["users"]
                    if user["id"] == result["author_id"]
                ]
                if matching_users:
                    formatted_results.append(
                        SearchResult(
                            id=result["id"],
                            username=matching_users[0]["username"],
                            text=result["text"],
                            retweet_count=public_metrics.get("retweet_count", 0),
                            reply_count=public_metrics.get("reply_count", 0),
                            like_count=public_metrics.get("like_count", 0),
                            quote_count=public_metrics.get("quote_count", 0),
                            bookmark_count=public_metrics.get("bookmark_count", 0),
                            impression_count=public_metrics.get("impression_count", 0),
                            referenced_tweets=result.get("referenced_tweets", []),
                            attachments=result.get("attachments"),
                        )
                    )
            return formatted_results
        except Exception:
            logger.error("Error searching tweets", exc_info=True)
            return []

    async def _make_request(
        self, method: Literal["GET", "POST"], endpoint: str, **kwargs
    ) -> Dict:
        # TODO: Should be async ideally
        logger.debug(f"Making {method} request to {endpoint}")
        try:
            oauth = self.oauth_session
            full_url = f"https://api.twitter.com/2/{endpoint.lstrip('/')}"

            response = getattr(oauth, method.lower())(full_url, **kwargs)

            if response.status_code not in [200, 201]:
                logger.error(
                    f"Request failed: {response.status_code} - {response.text}"
                )
                raise TwitterAPIError(
                    f"Request failed with status {response.status_code}: {response.text}"
                )

            logger.debug(f"Request successful: {response.status_code}")
            return response.json()

        except Exception as e:
            raise TwitterAPIError(f"API request failed: {str(e)}")
