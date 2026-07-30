"""Gemini File Search functions for the themed RAG assistant."""

import os
import time
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

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
    # TODO 1 - Connect to Gemini
    # Use: load_dotenv(), os.getenv("GEMINI_API_KEY"), and genai.Client(...)
    # Raise a clear ValueError when the key is missing.
    raise NotImplementedError("Complete TODO 1 to connect to Gemini.")


def create_file_search_store(client: Any, display_name: str) -> str:
    """Create a File Search store and return its resource name."""
    # TODO 2 - Create the File Search store
    # Use: client.file_search_stores.create(...)
    # Configure EMBEDDING_MODEL and return file_search_store.name.
    raise NotImplementedError("Complete TODO 2 to create a File Search store.")


def upload_documents(
    client: Any, file_search_store_name: str, documents: list[Path]
) -> None:
    """Upload every document and wait for indexing to finish."""
    # TODO 3 - Upload and process the documents
    # Check len(documents), then use upload_to_file_search_store(...) for each file.
    # Poll client.operations.get(operation) with time.sleep(...) until it is done.
    raise NotImplementedError("Complete TODO 3 to upload the documents.")


def ask_question(
    client: Any, file_search_store_name: str, question: str
) -> tuple[str, list[str]]:
    """Return a grounded answer and the unique source filenames."""
    # TODO 4 - Ask Gemini a grounded question
    # Use: client.interactions.create(...), MODEL_NAME, and the File Search tool.
    # Tell Gemini to use only the documents and to return FALLBACK_RESPONSE when needed.
    # Read model-output text and file-citation annotations from the response.
    raise NotImplementedError("Complete TODO 4 to answer questions.")
