def reciprocal_rank_fusion(result_lists, k=60):
    """
    Combine ranked results from multiple retrievers using RRF.
    """

    scores = {}
    documents = {}

    for results in result_lists:

        for rank, document in enumerate(results, start=1):

            # Use the document text as a simple unique identifier
            doc_id = document.page_content

            if doc_id not in scores:
                scores[doc_id] = 0
                documents[doc_id] = document

            scores[doc_id] += 1 / (k + rank)

    ranked_documents = sorted(
        documents.values(),
        key=lambda document: scores[document.page_content],
        reverse=True
    )

    return ranked_documents