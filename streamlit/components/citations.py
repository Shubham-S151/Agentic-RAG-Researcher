import streamlit as st

from typing import List, Dict, Any



def render_citations(
    citations: List[Dict[str, Any]]
):
    """
    Render source citations.

    Expected format:

    [
        {
            "title": "Attention Is All You Need",
            "page": 3,
            "doi": "10.xxxx/xxxx",
            "url": "https://..."
        }
    ]
    """


    if not citations:

        return



    st.divider()


    st.subheader(
        "📚 Sources"
    )


    for index, citation in enumerate(
        citations,
        start=1
    ):

        title = citation.get(
            "title",
            "Unknown Source"
        )


        page = citation.get(
            "page",
            None
        )


        doi = citation.get(
            "doi",
            None
        )


        url = citation.get(
            "url",
            None
        )


        with st.expander(
            f"[{index}] {title}"
        ):


            if page:

                st.write(
                    f"📄 Page: {page}"
                )


            if doi:

                st.write(
                    f"🔗 DOI: {doi}"
                )


            if url:

                st.markdown(
                    f"🌐 URL: {url}"
                )
