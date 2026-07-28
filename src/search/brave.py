import os

from typing import List, Dict, Any

import httpx

from src.search.base import SearchProvider

from src.config.logging import get_logger


logger = get_logger(__name__)


class BraveSearch(SearchProvider):
    """
    Brave Search API implementation.

    Responsibilities:

    - API authentication
    - HTTP communication
    - result normalization
    """


    def __init__(self):

        self.api_key = os.getenv(
            "BRAVE_API_KEY"
        )


        self.endpoint = (
            "https://api.search.brave.com/res/v1/web/search"
        )



    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Execute Brave web search.

        Returns:

        [
            {
                "title": "",
                "url": "",
                "content": ""
            }
        ]

        """


        if not self.api_key:

            logger.warning(
                "BRAVE_API_KEY missing"
            )

            return []



        headers = {

            "Accept":
                "application/json",


            "X-Subscription-Token":
                self.api_key,

        }



        params = {

            "q":
                query,


            "count":
                max_results,

        }



        try:

            async with httpx.AsyncClient(
                timeout=15.0
            ) as client:


                response = await client.get(

                    self.endpoint,

                    headers=headers,

                    params=params,

                )


                response.raise_for_status()



                data = response.json()



            results = []



            web_results = (
                data
                .get("web", {})
                .get("results", [])
            )



            for item in web_results:

                results.append(

                    {

                        "title":
                            item.get(
                                "title",
                                "",
                            ),


                        "url":
                            item.get(
                                "url",
                                "",
                            ),


                        "content":
                            item.get(
                                "description",
                                "",
                            ),

                    }

                )



            logger.info(

                "Brave returned %s results",

                len(results),

            )



            return results



        except httpx.HTTPError as error:


            logger.error(

                "Brave search failed: %s",

                error,

            )


            return []
