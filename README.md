# Stack Overflow RAG Q&A (Gemini Pro + Flutter)

A full-stack question-answering app using Retrieval-Augmented Generation (RAG) with Stack Overflow data, a Flask backend, Gemini Pro LLM, and a Flutter frontend.

## Backend
- Python Flask API for Q&A
- Supports local JSON and Hugging Face streaming (mikex86/stackoverflow-posts)
- Advanced ranking: sorts by accepted answer, score, and favorite count
- Returns tags, score, favorite count, and accepted answer ID for each result
- Gemini Pro for answer generation
- Unit and integration tests in `backend/tests`

### Setup
1. `cd backend`
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Add your API keys to `.env` (see PRD for example)
5. Run: `python app_main.py`

### Hugging Face Data
- Uses the `mikex86/stackoverflow-posts` dataset for streaming Q&A pairs.
- Results are ranked by accepted answer, score, and favorites.
- You can set `max_items` in the backend to control how many Q&A pairs are streamed.

### Testing
- Run all tests with:
  ```sh
  pytest tests/
  ```

## Frontend
- Flutter 3.x app in `/frontend`
- UI for asking questions, selecting Q&A source, and viewing answers with tags, score, favorites, and accepted answer badge

### Setup
1. `cd frontend`
2. `flutter pub get`
3. `flutter run` (web, Android, or iOS)

## API Example
POST `/ask`
```json
{ "question": "python", "source": "hf" }
```
Response:
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

See `PRD.md` for full requirements and details.

---

## Security & Project Hygiene
- `.gitignore` files are present in both backend and frontend to protect secrets and build artifacts.

## Next Steps
- Enhance frontend to allow filtering and display of tags, score, favorites, and accepted answer.
- Add more robust error handling and user feedback.

## Changelog
- [2025-07-01] Project initialized, backend and frontend scaffolded, secure .gitignore added.
- [2025-07-01] Backend supports advanced ranking and metadata for Hugging Face Q&A.

## Notes
- Backend can save Q&A requests/responses for analytics and future retrieval.
- Frontend allows users to select data source and compare results side-by-side.
- Data quality and success metrics can be visualized in the UI.
