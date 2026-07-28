from typing import Any, Dict, List

import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

from src.config.logging import get_logger
from src.config.settings import settings


logger = get_logger(__name__)


class CrossEncoderReranker:
    """
    Cross encoder based document reranker.

    Workflow:

        Query + Document

              |

              ▼

        Transformer Model

              |

              ▼

        Relevance Score

    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-reranker-large",
    ):

        self.model_name = model_name

        logger.info(
            "Loading reranker model: %s",
            model_name,
        )


        self.tokenizer = (
            AutoTokenizer.from_pretrained(
                model_name
            )
        )


        self.model = (
            AutoModelForSequenceClassification
            .from_pretrained(
                model_name
            )
        )


        self.model.eval()



    def rerank(
        self,
        query: str,
        documents: List[Dict[str, Any]],
        top_k: int | None = None,
    ) -> List[Dict[str, Any]]:
        """
        Reorder retrieved documents by relevance.

        Args:

            query:
                User question

            documents:
                Retrieved chunks from Qdrant

            top_k:
                Number of final documents

        Returns:

            Sorted documents with rerank scores
        """


        if not documents:
            return []


        pairs = [
            (
                query,
                document["text"],
            )

            for document in documents
        ]


        inputs = self.tokenizer(
            pairs,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors="pt",
        )


        with torch.no_grad():

            scores = (
                self.model(**inputs)
                .logits
                .squeeze()
                .tolist()
            )


        # Handle single document case
        if isinstance(
            scores,
            float,
        ):
            scores = [scores]


        for document, score in zip(
            documents,
            scores,
        ):

            document["rerank_score"] = (
                float(score)
            )


        ranked_documents = sorted(
            documents,
            key=lambda x: x["rerank_score"],
            reverse=True,
        )


        limit = (
            top_k
            or settings.top_k_rerank
        )


        return ranked_documents[:limit]
