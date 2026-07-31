"""Gemini File Search functions for the themed RAG assistant."""

import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Assuming these constants are defined in a config.py file
from config import (
    DATA_DIR,
    EMBEDDING_MODEL,
    FALLBACK_RESPONSE,
    MODEL_NAME,
    SUPPORTED_SUFFIXES,
)


def find_documents() -> list[Path]:
    """Return supported documents in the data folder."""
    DATA_DIR.mkdir(exist_ok=True)
    return sorted(
        path
        for path in DATA_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )


def create_gemini_client() -> Any:
    """Load the API key and return a Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY inside your .env file.")
    return genai.Client(api_key=api_key)


def create_file_search_store(client: Any, display_name: str) -> str:
    """Create a File Search store and return its resource name."""
    file_search_store = client.file_search_stores.create(
        config=types.FileSearchStoreConfig(
            display_name=display_name,
            embedding_model=EMBEDDING_MODEL
        )
    )
    return file_search_store.name


def upload_documents(
        client: Any, file_search_store_name: str, documents: list[Path]
) -> None:
    """Upload documents and wait for indexing, similar to Google's file search implementation."""
    if not documents:
        return
    for doc_path in documents:
        upload_op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=file_search_store_name,
            file=str(doc_path),
            config=types.UploadToFileSearchStoreConfig(display_name=doc_path.name)
        )
        # Poll for completion
        while not (upload_op := client.operations.get(upload_op)).done:
            time.sleep(2)


def ask_question(
        client: Any, file_search_store_name: str, question: str
) -> tuple[str, list[str]]:
    """Grounded Q&A using Gemini's file search, extracting sources from citations."""
    file_search_tool = types.Tool(
        file_search=types.FileSearch(file_search_stores=[file_search_store_name])
    )

    system_instruction = (
        f"Answer using ONLY the provided documents. "
        f"If not found, respond exactly: '{FALLBACK_RESPONSE}'."
    )

    # Perform interaction with strict grounding
    interaction = client.interactions.create(
        model=MODEL_NAME,
        input=question,
        tools=[file_search_tool],
        config=types.InteractionConfig(
            system_instruction=system_instruction,
            temperature=0.0
        )
    )

    # Parse output and extract sources from annotations
    output_text = interaction.outputs[-1].text if interaction.outputs else FALLBACK_RESPONSE
    source_filenames = set()
    if interaction.outputs:
        for output in interaction.outputs:
            if hasattr(output, 'annotations') and output.annotations:
                for annotation in output.annotations:
                    if hasattr(annotation, 'file_citation') and annotation.file_citation:
                        doc_name = getattr(annotation.file_citation, 'file_search_store_document_display_name', None)
                        if doc_name:
                            source_filenames.add(doc_name)
    return output_text, sorted(list(source_filenames))