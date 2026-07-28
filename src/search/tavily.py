import os

from typing import List, Dict, Any

import httpx

from src.search.base import SearchProvider

from src.config.logging import get_logger


logger = get_logger(__name__)



class TavilySearch(SearchProvider):
    """
    Tavily API implementation.

    Responsible for:

    - API communication
    - error handling
    - response normalization
    """


    def __init__(self):

        self.api_key = os.getenv(
            "TAVILY_API_KEY"
        )

        self.endpoint = (
            "https://api.tavily.com/search"
        )



    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Execute Tavily web search.

        Returns normalized format:

        [
            {
                title:"",
                url:"",
                content:""
            }
        ]

        """


        if not self.api_key:

            logger.warning(
                "TAVILY_API_KEY missing"
            )

            return []



        payload = {

            "api_key":
                self.api_key,


            "query":
                query,


            "search_depth":
                "advanced",


            "max_results":
                max_results,


            "include_answer":
                False,
        }



        try:

            async with httpx.AsyncClient(
                timeout=15.0
            ) as client:


                response = await client.post(

                    self.endpoint,

                    json=payload,

                )


                response.raise_for_status()



                data = response.json()



            results = []



            for item in data.get(
                "results",
                []
            ):

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
                                "content",
                                "",
                            ),

                    }

                )



            logger.info(

                "Tavily returned %s results",

                len(results),

            )



            return results



        except httpx.HTTPError as error:


            logger.error(

                "Tavily search failed: %s",

                error,

            )


            return []
