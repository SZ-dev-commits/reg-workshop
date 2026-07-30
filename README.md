# RAG Assistant with Gemini File Search

A Retrieval-Augmented Generation (RAG) assistant built with Google Gemini's File Search API and Streamlit. This application allows you to upload documents and ask questions about them with grounded, source-cited answers.

## Features

- **Document Upload**: Support for `.txt` and `.md` files
- **Grounded Answers**: Responses are strictly based on uploaded documents
- **Source Citation**: Displays which documents were used for each answer
- **Fallback Handling**: Gracefully handles questions outside document scope
- **Modern UI**: Clean Streamlit interface with sidebar document management

## Requirements

- Python 3.11 or newer
- Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rag-workshop
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # or
   source .venv/bin/activate  # On macOS/Linux
   ```

3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Replace `your_key_here` with your Gemini API key
   - Never commit `.env` to version control

## Usage

1. Add your documents to the `data/` folder (at least two `.txt` or `.md` files)

2. Start the application:
   ```bash
   streamlit run app.py
   ```

3. In the browser:
   - Click "Prepare document library" to upload and index your documents
   - Ask questions in the text input field
   - View answers with source citations

## Project Structure

```
rag-workshop/
├── app.py              # Streamlit interface
├── rag.py              # Gemini API and RAG logic
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── data/               # Document storage folder
└── README.md          # This file
```

## Configuration

Edit `config.py` to customize:
- `APP_TITLE`: Application title
- `APP_DESCRIPTION`: Application description
- `MODEL_NAME`: Gemini model to use
- `EMBEDDING_MODEL`: Embedding model for document indexing
- `FALLBACK_RESPONSE`: Message when answer is not found

## Troubleshooting

- **No documents found**: Ensure files are in `data/` and have `.txt` or `.md` extensions
- **Missing API key**: Check that `.env` file exists and contains `GEMINI_API_KEY`
- **Upload appears stuck**: Document processing may take time; be patient
- **Wrong answers**: Strengthen grounding instructions in `rag.py` for better accuracy

## API Reference

- [Gemini File Search Documentation](https://ai.google.dev/gemini-api/docs/file-search)
- [Streamlit Documentation](https://docs.streamlit.io/)

## License

This project is provided as-is for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.
