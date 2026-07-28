from typing import Any, Dict, List

from rank_bm25 import BM25Okapi

from src.config.logging import get_logger


logger = get_logger(__name__)


class HybridRetriever:
    """
    Hybrid retrieval combining:

    1. Semantic vector retrieval
    2. Keyword BM25 retrieval

    Final ranking uses reciprocal rank fusion.
    """


    def __init__(
        self,
        vector_retriever,
    ):

        self.vector_retriever = (
            vector_retriever
        )

        self.documents = []


        self.bm25 = None



    def build_keyword_index(
        self,
        documents: List[Dict[str, Any]],
    ):
        """
        Build BM25 index from documents.

        Called during ingestion.
        """


        self.documents = documents


        tokenized_docs = [

            doc["text"]
            .lower()
            .split()

            for doc in documents
        ]


        self.bm25 = BM25Okapi(
            tokenized_docs
        )


        logger.info(
            "BM25 index created with %s documents",
            len(documents),
        )



    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Execute hybrid retrieval.

        Returns combined ranked results.
        """


        # --------------------------------
        # Vector retrieval
        # --------------------------------

        semantic_results = (
            await self.vector_retriever.retrieve(
                query=query,
                top_k=top_k,
            )
        )


        # --------------------------------
        # BM25 retrieval
        # --------------------------------

        keyword_results = (
            self.keyword_search(
                query=query,
                top_k=top_k,
            )
        )


        # --------------------------------
        # Reciprocal Rank Fusion
        # --------------------------------

        fused_results = (
            self.reciprocal_rank_fusion(
                [
                    semantic_results,
                    keyword_results,
                ]
            )
        )


        return fused_results[:top_k]



    def keyword_search(
        self,
        query: str,
        top_k: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Traditional lexical retrieval.
        """


        if not self.bm25:
            return []


        scores = self.bm25.get_scores(
            query.lower().split()
        )


        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )


        results = []


        for idx in ranked_indices[:top_k]:

            document = (
                self.documents[idx]
                .copy()
            )


            document["keyword_score"] = (
                float(scores[idx])
            )


            results.append(
                document
            )


        return results



    def reciprocal_rank_fusion(
        self,
        result_lists: List[List[Dict[str, Any]]],
        k: int = 60,
    ) -> List[Dict[str, Any]]:
        """
        Combines rankings from multiple retrievers.

        RRF formula:

        score =
            Σ 1 / (k + rank)

        """

        fused = {}


        for results in result_lists:

            for rank, doc in enumerate(
                results
            ):

                doc_id = (
                    doc.get("id")
                    or doc["text"][:100]
                )


                if doc_id not in fused:

                    fused[doc_id] = {
                        **doc,
                        "fusion_score": 0,
                    }


                fused[doc_id][
                    "fusion_score"
                ] += (
                    1 / (k + rank + 1)
                )


        return sorted(
            fused.values(),
            key=lambda x: x["fusion_score"],
            reverse=True,
        )
