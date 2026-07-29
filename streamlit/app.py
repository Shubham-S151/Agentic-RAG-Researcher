import streamlit as st

from utils import query_agent
from components.chat import render_chat_message
from components.citations import render_citations



# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="Agentic RAG Researcher",
    page_icon="📚",
    layout="wide",
)



# -----------------------------------------------------
# Header
# -----------------------------------------------------

st.title(
    "📚 Agentic-RAG Researcher"
)

st.caption(
    "Hybrid RAG system with local papers, web search, "
    "reranking and citation-aware generation."
)



# -----------------------------------------------------
# Session State
# -----------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []



# -----------------------------------------------------
# Display Previous Messages
# -----------------------------------------------------

for message in st.session_state.messages:

    render_chat_message(
        role=message["role"],
        content=message["content"]
    )



# -----------------------------------------------------
# User Input
# -----------------------------------------------------

query = st.chat_input(
    "Ask about research papers or current AI topics..."
)



if query:

    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    render_chat_message(
        role="user",
        content=query
    )


    with st.spinner(
        "Agent is thinking..."
    ):

        response = query_agent(
            query
        )


    answer = response.get(
        "answer",
        "No response generated."
    )


    route = response.get(
        "route_taken",
        "unknown"
    )


    citations = response.get(
        "citations",
        []
    )


    # Display route information

    st.info(
        f"Execution route: {route}"
    )


    render_chat_message(
        role="assistant",
        content=answer
    )


    if citations:

        render_citations(
            citations
        )


    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
