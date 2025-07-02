# Stack Overflow RAG Q&A Backend

## Requirements
- Python 3.11 recommended for best compatibility (use `python3.11` for venv)

## Setup
1. `cd backend`
2. `python3.11 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and add your API keys
5. Run: `python app_main.py`

## Hugging Face Data Integration
- The backend streams Stack Overflow Q&A pairs from Hugging Face (`mikex86/stackoverflow-posts`).
- Results are ranked by accepted answer, score, and favorites, and include tags and metadata.
- You can adjust `max_items` in the backend for faster or broader search.

## API Usage
- POST `/ask` with:
  ```json
  { "question": "python", "source": "hf" }
  ```
- Response includes:
  ```json
  {
    "answer": "...",
    "sources": [
      {
        "question": "...",
        "answer": "...",
        "tags": ["python", "list"],
        "score": 120,
        "favorite_count": 15,
        "accepted_answer_id": 123456
      }
    ],
    "tokens": 312,
    "status": "done"
  }
  ```

## Testing
Run all tests with:
```
pytest tests/
```

---

# Stack Overflow RAG Q&A Frontend

## Setup
1. `cd frontend`
2. `flutter pub get`
3. `flutter run` (web, Android, or iOS)

## Notes
- The frontend UI displays tags, score, favorites, and accepted answer badge for each result.
- Users can select the Q&A data source and compare results.
