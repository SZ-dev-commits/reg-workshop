"""Streamlit interface for the themed RAG assistant."""

import streamlit as st

from config import APP_DESCRIPTION, APP_TITLE
from rag import (
    ask_question,
    create_file_search_store,
    create_gemini_client,
    find_documents,
    upload_documents,
)


def show_sidebar() -> None:
    """Display the documents and prepare the File Search library."""
    documents = find_documents()

    with st.sidebar:
        st.header("Document library")
        if documents:
            for document in documents:
                st.write(f"- {document.name}")
        else:
            st.info("Add at least two .txt or .md files to the data folder.")

        st.divider()
        st.caption(f"{len(documents)} supported document(s) found")

        if st.button("Prepare document library", use_container_width=True):
            try:
                client = create_gemini_client()
                store_name = create_file_search_store(
                    client, f"{APP_TITLE} document store"
                )
                upload_documents(client, store_name, documents)
                st.session_state["client"] = client
                st.session_state["store_name"] = store_name
                st.success("The document library is ready.")
            except (NotImplementedError, ValueError) as error:
                st.warning(str(error))
            except Exception as error:
                st.error(f"Could not prepare the document library: {error}")


def main() -> None:
    """Render the application."""
    st.set_page_config(page_title=APP_TITLE, page_icon="🔎")
    st.title(APP_TITLE)
    st.write(APP_DESCRIPTION)
    show_sidebar()

    question = st.text_input(
        "What would you like to know?",
        placeholder="Ask a question that your documents can answer...",
    )

    if st.button("Ask", type="primary"):
        client = st.session_state.get("client")
        store_name = st.session_state.get("store_name")

        if not question.strip():
            st.warning("Enter a question first.")
        elif client is None or store_name is None:
            st.warning("Prepare the document library before asking a question.")
        else:
            try:
                answer, sources = ask_question(client, store_name, question.strip())
                st.subheader("Answer")
                st.write(answer)

                st.subheader("Sources")
                if sources:
                    for source in sources:
                        st.write(f"- {source}")
                else:
                    st.write("No source files were returned.")
            except NotImplementedError as error:
                st.warning(str(error))
            except Exception as error:
                st.error(f"Could not answer the question: {error}")


if __name__ == "__main__":
    main()
