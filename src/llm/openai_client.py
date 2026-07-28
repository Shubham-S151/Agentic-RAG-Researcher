from typing import Optional

from openai import AsyncOpenAI
from openai import APIError, APITimeoutError, RateLimitError

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


class OpenAIClient:
    """
    Production wrapper around OpenAI async client.

    All LLM communication should go through this class.
    """


    def __init__(
        self,
        client: Optional[AsyncOpenAI] = None,
    ):
        self.client = client or AsyncOpenAI(
            api_key=settings.openai_api_key
        )

        self.generation_model = (
            settings.generation_model
        )

        self.router_model = (
            settings.router_model
        )


    async def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: float = 0.2,
    ) -> str:
        """
        Generate text completion.

        Used for:
        - Answer generation
        - Query rewriting
        - Verification
        """


        selected_model = (
            model
            if model
            else self.generation_model
        )


        try:

            response = await self.client.chat.completions.create(

                model=selected_model,

                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],

                temperature=temperature,
            )


            return (
                response
                .choices[0]
                .message
                .content
                or ""
            )


        except RateLimitError:

            logger.exception(
                "OpenAI rate limit exceeded"
            )

            raise


        except APITimeoutError:

            logger.exception(
                "OpenAI request timeout"
            )

            raise


        except APIError:

            logger.exception(
                "OpenAI API failure"
            )

            raise


    async def route_query(
        self,
        prompt: str,
    ) -> str:
        """
        Lightweight model call for routing.

        Uses cheaper model because routing
        does not require large generation ability.
        """

        return await self.generate(
            prompt=prompt,
            model=self.router_model,
            temperature=0,
        )
