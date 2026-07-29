"""
Run Agentic-RAG evaluation pipeline.

Workflow:

1. Load evaluation questions
2. Execute RAG agent
3. Collect answers and contexts
4. Run Ragas metrics
5. Save evaluation results
"""


import asyncio
import json

from pathlib import Path


from src.graph.graph import runtime_agent

from src.evaluation.ragas_eval import (
    ragas_evaluator,
)

from src.config.logging import get_logger



logger = get_logger(__name__)



DATASET_PATH = Path(
    "data/evaluation/questions.json"
)


OUTPUT_PATH = (
    "evaluation/results/ragas_results.csv"
)



async def run_agent_query(
    question: str
):
    """
    Execute Agentic RAG pipeline.
    """


    initial_state = {

        "query": question,

        "route_decision": "",

        "retrieved_documents": [],

        "web_results": [],

        "compiled_context": "",

        "generation": "",

        "citation_mappings": [],

        "retry_count": 0,

        "is_hallucination": False,

    }



    result = await runtime_agent.ainvoke(
        initial_state
    )


    return result



async def create_ragas_samples():

    """
    Convert agent outputs into Ragas format.
    """


    with open(
        DATASET_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        questions = json.load(
            file
        )



    samples = []



    for item in questions:


        question = item["question"]


        logger.info(
            "Evaluating: %s",
            question
        )



        response = await run_agent_query(
            question
        )



        contexts = []


        for document in response.get(
            "retrieved_documents",
            []
        ):

            contexts.append(
                document.get(
                    "text",
                    ""
                )
            )



        samples.append(

            {

                "question": question,

                "answer":
                response.get(
                    "generation",
                    ""
                ),

                "contexts": contexts,

                "ground_truth":
                item.get(
                    "ground_truth",
                    ""
                )

            }

        )


    return samples



async def main():

    samples = await create_ragas_samples()



    logger.info(
        "Running Ragas evaluation..."
    )


    result = ragas_evaluator.evaluate(
        samples
    )



    ragas_evaluator.print_summary(
        result
    )


    ragas_evaluator.save_results(

        result,

        OUTPUT_PATH

    )


    logger.info(
        "Evaluation completed."
    )



if __name__ == "__main__":

    asyncio.run(
        main()
    )
