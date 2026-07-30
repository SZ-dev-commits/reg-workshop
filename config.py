"""Settings students can personalise after the RAG flow works."""

from pathlib import Path


APP_TITLE = "My Themed RAG Assistant"
APP_DESCRIPTION = "Ask questions about the documents in this assistant's library."

DATA_DIR = Path(__file__).parent / "data"
SUPPORTED_SUFFIXES = {".md", ".txt"}

FALLBACK_RESPONSE = "I couldn't find that information in the provided documents."
MODEL_NAME = "models/gemini-3.6-flash"
EMBEDDING_MODEL = "models/gemini-embedding-2"
