import os

from typing import Optional

from openai import AsyncOpenAI

from src.config.logging import get_logger


logger = get_logger(__name__)


class OpenAIClient:
    """
    Async wrapper around OpenAI API.

    Responsibilities:

    - Client initialization
    - Model configuration
    - Prompt execution
    - Error handling
    """


    def __init__(self):

        self.client = AsyncOpenAI(
            api_key=os.getenv(
                "OPENAI_API_KEY"
            )
        )


        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-4o-mini"
        )


        self.temperature = float(
            os.getenv(
                "LLM_TEMPERATURE",
                "0.1"
            )
        )



    async def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Execute async chat completion.

        Returns:

        Generated text response.
        """


        messages = []



        if system_prompt:

            messages.append(

                {
                    "role":
                    "system",

                    "content":
                    system_prompt
                }

            )



        messages.append(

            {
                "role":
                "user",

                "content":
                prompt
            }

        )



        try:

            response = await self.client.chat.completions.create(

                model=self.model,

                messages=messages,

                temperature=self.temperature,

            )



            result = (
                response
                .choices[0]
                .message
                .content
            )



            logger.info(
                "LLM generation successful"
            )


            return result or ""



        except Exception as error:


            logger.error(

                "LLM request failed: %s",

                error,

            )


            raise



    async def structured_output(
        self,
        prompt: str,
    ):
        """
        Generate JSON structured responses.

        Used by:

        - Router
        - Evaluator
        - Verification agents
        """


        try:

            response = await self.client.chat.completions.create(

                model=self.model,

                messages=[
                    {
                        "role":
                        "user",

                        "content":
                        prompt
                    }
                ],


                response_format={
                    "type":
                    "json_object"
                },


                temperature=0,

            )


            return response.choices[0].message.content



        except Exception as error:


            logger.error(

                "Structured LLM call failed: %s",

                error,

            )


            raise



# Singleton instance
# Imported by graph nodes

llm_client = OpenAIClient()
