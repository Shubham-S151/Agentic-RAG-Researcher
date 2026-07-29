import streamlit as st



def render_chat_message(
    role: str,
    content: str,
):
    """
    Render a chat message bubble.

    Args:
        role:
            user or assistant

        content:
            message text
    """

    if role == "user":

        with st.chat_message(
            "user"
        ):

            st.markdown(
                content
            )


    elif role == "assistant":

        with st.chat_message(
            "assistant"
        ):

            st.markdown(
                content
            )


    else:

        with st.chat_message(
            "assistant"
        ):

            st.warning(
                content
            )
