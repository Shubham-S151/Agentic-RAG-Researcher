"""
Evaluation utilities for the Agentic-RAG system.

Uses the Ragas framework to evaluate retrieval
and generation quality.
"""

from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from datasets import Dataset

from ragas import evaluate

from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)


class RAGASEvaluator:
    """
    Wrapper around Ragas evaluation.

    Expected input format:

    [
        {
            "question": "...",
            "answer": "...",
            "contexts": [...],
            "ground_truth": "..."
        }
    ]
    """

    def __init__(self):

        self.metrics = [

            faithfulness,

            answer_relevancy,

            context_precision,

            context_recall,

        ]

    def evaluate(
        self,
        samples: List[Dict[str, Any]],
    ):

        dataset = Dataset.from_list(samples)

        return evaluate(
            dataset=dataset,
            metrics=self.metrics,
        )

    def evaluate_from_dataframe(
        self,
        dataframe: pd.DataFrame,
    ):

        dataset = Dataset.from_pandas(dataframe)

        return evaluate(
            dataset=dataset,
            metrics=self.metrics,
        )

    def save_results(
        self,
        evaluation_result,
        output_path: str,
    ):

        output = Path(output_path)

        output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        dataframe = evaluation_result.to_pandas()

        dataframe.to_csv(
            output,
            index=False,
        )

    def print_summary(
        self,
        evaluation_result,
    ):

        dataframe = evaluation_result.to_pandas()

        print()

        print("=" * 60)

        print("RAGAS Evaluation Summary")

        print("=" * 60)

        print(dataframe.mean(numeric_only=True))

        print("=" * 60)


ragas_evaluator = RAGASEvaluator()
