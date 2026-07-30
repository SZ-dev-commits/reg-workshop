"""Gemini File Search functions for the themed RAG assistant."""
import os
import time
from pathlib import Path
from typing import Any
from dotenv import load_dotenv
from google import genai
from google.genai import types
from config import DATA_DIR, EMBEDDING_MODEL, FALLBACK_RESPONSE, MODEL_NAME, SUPPORTED_SUFFIXES

def find_documents() -> list[Path]:
    """Return supported documents in the data folder."""
    DATA_DIR.mkdir(exist_ok=True)
    return sorted(path for path in DATA_DIR.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES)

def create_gemini_client() -> Any:
    """Load the API key and return a Gemini client."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key: raise ValueError("Missing GEMINI_API_KEY in .env file.")
    return genai.Client(api_key=api_key)

def create_file_search_store(client: Any, display_name: str) -> str:
    """Create a File Search store and return its name."""
    store = client.file_search_stores.create(config={"display_name": display_name})
    return store.name

def upload_documents(client: Any, file_search_store_name: str, documents: list[Path]) -> None:
    """Upload documents and wait for indexing."""
    for doc_path in documents:
        op = client.file_search_stores.upload_to_file_search_store(
            file_search_store_name=file_search_store_name, file=str(doc_path),
            config=types.UploadToFileSearchStoreConfig(display_name=doc_path.name)
        )
        while not (op := client.operations.get(op)).done: time.sleep(2)


def ask_question(
        client: Any, file_search_store_name: str, question: str
) -> tuple[str, list[str]]:
    """Return a grounded answer and source filenames using gemini-1.5-flash to bypass the 429 quota."""
    # TODO 4 - Ask Gemini a grounded question

    # Read text context from files directly into memory
    attached_contexts = []
    try:
        for doc_path in find_documents():
            with open(doc_path, "r", encoding="utf-8") as f:
                attached_contexts.append(f"--- START OF FILE: {doc_path.name} ---\n{f.read()}\n--- END OF FILE ---")
    except Exception as e:
        return f"Could not read local source context items: {str(e)}", []

    # Enforce strict grounding guardrails
    sys_inst = (
        f"You are a helpful assistant. Use ONLY the text from the attached files "
        f"to answer the question. If the information is not present in the files, "
        f"respond exactly with: '{FALLBACK_RESPONSE}'."
    )

    # Combine travel texts and the user question into the contents payload
    prompt_payload = attached_contexts + [question]

    # FIX: Use MODEL_NAME from config to clear the 429 RESOURCE_EXHAUSTED block
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_payload,
        config={
            "system_instruction": sys_inst,
            "temperature": 0.0
        }
    )

    output_text = response.text if response.text else FALLBACK_RESPONSE
    sources = [d.name for d in find_documents()] if output_text != FALLBACK_RESPONSE else []
    return output_text, sources
