# Build Your Own Themed RAG Assistant

## What you will build

Your finished assistant will:

- use at least two `.txt` or `.md` documents;
- answer questions using Gemini File Search;
- display the filenames used as sources;
- say when an answer is unavailable; and
- have a theme and at least two personal improvements.

## Set up the project

You need Python 3.11 or newer and a Gemini API key.

1. Install the packages:

   ```bash
   python -m pip install -r requirements.txt
   ```

2. Copy `.env.example` to a new file named `.env`. Replace
   `your_key_here` with your Gemini API key. Never put the key directly in
   a Python file, share it, or commit `.env`.

3. Add at least two themed `.txt` or `.md` files to `data/`.

4. Start the app:

   ```bash
   streamlit run app.py
   ```

The starter launches before the TODOs are complete. It will tell you which
task is still unfinished.

## Complete the worksheet tasks

The four coding TODOs match worksheet Steps 4-7:

1. Connect to Gemini in `rag.py`.
2. Create a theme-specific File Search store in `rag.py`.
3. Upload and process every document in `rag.py`.
4. Ask grounded questions and collect cited filenames in `rag.py`.

The Streamlit interface in `app.py` is already complete. You do not need to
understand Streamlit to complete the RAG tasks. For worksheet Step 8, run the
app and check that an answer and its source filenames appear on the page.

The project is split into three small Python files:

- `app.py` contains the completed Streamlit interface.
- `rag.py` contains the Gemini and document-search code.
- `config.py` contains the settings you can personalise.

Use the hints beside each TODO and the
[Gemini File Search documentation](https://ai.google.dev/gemini-api/docs/file-search)
when you need to check an API call.

## Test your assistant

Before personalising the design, check all of these:

- The sidebar lists at least two documents.
- **Prepare document library** finishes successfully.
- A question covered by the documents produces a useful answer.
- The source filenames appear below the answer.
- A question not covered by the documents produces:
  `I couldn't find that information in the provided documents.`
- The API key is present only in `.env`.

## Troubleshooting

- **No documents found:** Check that the files are directly inside `data/` and
  end in `.txt` or `.md`.
- **Missing API key:** Check that the file is named exactly `.env` and the
  variable is named `GEMINI_API_KEY`.
- **Upload appears stuck:** Processing can take a little time. Make sure TODO 3
  refreshes the operation while waiting.
- **Wrong or unsupported answers:** Strengthen the grounding instructions in
  TODO 4 and test with a question whose answer is absent from every document.
