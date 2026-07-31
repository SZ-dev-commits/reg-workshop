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
    print(f"[1/5] 🔍 Scanning directory for documents: {DATA_DIR}...", flush=True)

    docs = sorted(
        path
        for path in DATA_DIR.iterdir()
        if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )

    print(f"      ▶ Found {len(docs)} supported document(s).", flush=True)
    return docs


def create_gemini_client() -> Any:
    """Load the API key and return a Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY inside your .env file.")

    print("[2/5] 🔌 Initializing Gemini GenAI client...", flush=True)
    return genai.Client(api_key=api_key)


def create_file_search_store(client: Any, display_name: str) -> str:
    """Create a File Search store and return its resource name."""
    print(f"[3/5] 🏗️ Creating vector store in cloud (Name: {display_name})...", flush=True)

    # FIXED: Using raw dictionary to fix the AttributeError
    file_search_store = client.file_search_stores.create(
        config={
            "display_name": display_name,
            "embedding_model": EMBEDDING_MODEL
        }
    )

    print(f"      ▶ Store created successfully. ID: {file_search_store.name}", flush=True)
    return file_search_store.name


def upload_documents(
        client: Any, file_search_store_name: str, documents: list[Path]
) -> None:
    """Upload documents and wait for indexing, similar to Google's file search implementation."""
    if not documents:
        print("[4/5] ⚠️ No documents provided for upload. Skipping.", flush=True)
        return

    print(f"[4/5] 📤 Uploading and indexing {len(documents)} file(s)...", flush=True)
    for doc_path in documents:
        print(f"      -> Uploading file: {doc_path.name}", flush=True)

        # FIXED: Using raw dictionary to fix the AttributeError
        upload_op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=file_search_store_name,
            file=str(doc_path),
            config={"display_name": doc_path.name}
        )

        print(f"      ⏳ Waiting for cloud embedding indexation...", flush=True)
        while not (upload_op := client.operations.get(upload_op)).done:
            time.sleep(2)

    print("      ▶ ✨ All files successfully indexed!", flush=True)


def ask_question(
        client: Any, file_search_store_name: str, question: str
) -> tuple[str, list[str]]:
    """Grounded Q&A using Gemini's file search, extracting sources from citations."""
    print(f"\n[5/5] 💬 Received question: \"{question}\"", flush=True)
    print(f"      🔍 Querying vector store and generating response...", flush=True)

    file_search_tool = {
        "file_search": {
            "file_search_store_names": [file_search_store_name]
        }
    }

    system_instruction = (
        f"Answer using ONLY the provided documents. "
        f"If not found, respond exactly: '{FALLBACK_RESPONSE}'."
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=question,
        config={
            "tools": [file_search_tool],
            "system_instruction": system_instruction,
            "temperature": 0.0
        }
    )

    output_text = response.text if response.text else FALLBACK_RESPONSE
    source_filenames = set()

    # FIXED: Re-engineered metadata extraction logic with fallback attribute checks
    if response.candidates:
        for candidate in response.candidates:
            if candidate.grounding_metadata and candidate.grounding_metadata.grounding_chunks:
                for chunk in candidate.grounding_metadata.grounding_chunks:
                    # 1. Check for standard unencrypted display names or sources
                    doc_name = getattr(chunk, 'source', None)

                    # 2. Check for restricted source block with correct spelling
                    if not doc_name and hasattr(chunk, 'restricted_source') and chunk.restricted_source:
                        doc_name = getattr(chunk.restricted_source, 'display_name', None)

                    # 3. Check raw dictionary structure if present
                    if not doc_name and isinstance(chunk, dict):
                        doc_name = chunk.get('source') or chunk.get('restricted_source', {}).get('display_name')

                    if doc_name:
                        source_filenames.add(str(doc_name))

    print(f"      ✅ Answer generated.", flush=True)
    print(f"      📄 Citations used: {list(source_filenames)}", flush=True)
    return output_text, sorted(list(source_filenames))







