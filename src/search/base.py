from abc import ABC, abstractmethod
from typing import List, Dict, Any


class SearchProvider(ABC):
    """
    Abstract interface for web search providers.

    Any search engine implementation must
    follow this contract.
    """


    @abstractmethod
    async def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Execute web search.

        Returns:

        [
            {
                "title": "...",
                "url": "...",
                "content": "..."
            }
        ]

        """

        pass
