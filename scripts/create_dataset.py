"""
Create evaluation dataset for Agentic-RAG.

Output:

data/evaluation/questions.json


Dataset format:

[
    {
        "question": "...",
        "ground_truth": "...",
        "contexts": []
    }
]
"""


import json

from pathlib import Path



OUTPUT_PATH = Path(
    "data/evaluation/questions.json"
)



def create_dataset():

    """
    Creates initial evaluation benchmark.

    In production this can be generated from:
    - expert annotations
    - research paper QA generation
    - synthetic LLM generation
    """



    samples = [

        {

            "question":
            "What problem does retrieval augmented generation solve?",


            "ground_truth":
            (
                "Retrieval augmented generation improves "
                "LLM responses by providing external knowledge "
                "retrieved from documents instead of relying "
                "only on model parameters."
            ),


            "contexts":
            []

        },


        {

            "question":
            "Explain the purpose of vector embeddings in RAG systems.",


            "ground_truth":
            (
                "Vector embeddings convert text into numerical "
                "representations that allow semantic similarity "
                "search over documents."
            ),


            "contexts":
            []

        },


        {

            "question":
            "Why is reranking useful in retrieval pipelines?",


            "ground_truth":
            (
                "Reranking improves retrieval quality by using "
                "a stronger relevance model to reorder retrieved "
                "documents before generation."
            ),


            "contexts":
            []

        },


        {

            "question":
            "What are the benefits of hybrid search in RAG?",


            "ground_truth":
            (
                "Hybrid search combines lexical retrieval and "
                "semantic vector retrieval to improve recall "
                "across different query types."
            ),


            "contexts":
            []

        }

    ]



    OUTPUT_PATH.parent.mkdir(

        parents=True,

        exist_ok=True

    )



    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(

            samples,

            file,

            indent=4,

            ensure_ascii=False

        )



    print(
        f"Dataset created at {OUTPUT_PATH}"
    )



if __name__ == "__main__":

    create_dataset()
