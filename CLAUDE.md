# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Stack Overflow RAG (Retrieval-Augmented Generation) Q&A application backend built with Flask. The system streams Q&A pairs from Hugging Face, supports local JSON data, and uses Gemini Pro for answer generation. Results are ranked by accepted answer, score, and favorites, and include tags and metadata.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file with):
# GEMINI_API_KEY=your_gemini_api_key
```

### Running the Application
```bash
# Start the Flask server
python app_main.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_api.py

# Run with verbose output
pytest -v
```

## Architecture

### Core Components

**stream_hf_qa (app_main.py)**
- Streams Q&A pairs from Hugging Face (`mikex86/stackoverflow-posts`)
- Matches on title, body, or tags
- Sorts by accepted answer, score, and favorites
- Returns tags, score, favorite count, and accepted answer ID

**API Layer (app_main.py)**
- Single `/ask` endpoint accepting questions with configurable data sources
- Returns structured responses with answer, sources, tags, score, favorites, accepted answer, and token usage

**LLM Integration (app/gemini.py)**
- Wraps Gemini Pro API calls for answer generation
- Uses retrieved Q&A pairs as context in prompts
- Tracks token usage when available

### Key Data Structures

**Request Format:**
```json
{
  "question": "string",
  "source": "local|hf|llm"
}
```

**Response Format:**
```json
{
  "answer": "string",
  "sources": [{
    "question": "...",
    "answer": "...",
    "tags": ["python", "list"],
    "score": 120,
    "favorite_count": 15,
    "accepted_answer_id": 123456
  }],
  "tokens": 123,
  "status": "done"
}
```

## Configuration

The application uses environment variables loaded from `.env`:
- `GEMINI_API_KEY`: Required for LLM answer generation

## Data Sources

1. **Local**: Uses `data/localdata.json` file
2. **Hugging Face**: Streams from 'mikex86/stackoverflow-posts' dataset
3. **LLM**: Placeholder for future direct LLM integration

## Testing Strategy

Tests are located in `tests/` directory:
- `test_api.py`: API endpoint testing with both local and HF data sources

## Logging

Console logging is used for streaming, matching, and error handling in the backend.