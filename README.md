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

# Stack Overflow RAG Q&A

This project is a full-stack application for question answering using Stack Overflow data, with Retrieval-Augmented Generation (RAG) and LLM support.

## Project Structure

- `frontend/` — Flutter app (UI)
- `backend/`  — Python backend (Flask API)

## Prerequisites

- Python 3.8+
- pip
- Flutter SDK (3.x recommended)
- Dart SDK (comes with Flutter)
- Node.js (optional, for some dev tools)

## Backend Setup (Flask)

1. Open a terminal and navigate to the `backend/` directory:
   ```sh
   cd backend
   ```
2. Install dependencies:
   ```sh
   pip install flask flask-cors
   ```
3. Start the Flask API server:
   ```sh
   python flask_app.py
   ```
   The backend will run on `http://127.0.0.1:8001`.

## Frontend Setup (Flutter)

1. Open a new terminal and navigate to the `frontend/` directory:
   ```sh
   cd frontend
   ```
2. Install dependencies:
   ```sh
   flutter pub get
   ```
3. Run the Flutter app (macOS example):
   ```sh
   flutter run
   ```
   - For web: `flutter run -d chrome`
   - For iOS/Android: use your preferred device/emulator

## Usage

- Enter a programming question in the input box.
- Select a data source (Local, Hugging Face, or LLM).
- Click **Ask** to retrieve answers.
- Click **Generate LLM Answer** to get an answer from the LLM (calls Flask `/ask_llm`).
- Click the refresh button (top right) to clear and reset the app.

## Testing

- Ensure both backend and frontend are running.
- Try asking questions and generating LLM answers.
- The LLM answer and its source link will appear below the main answer.

## Notes

- The LLM answer is currently a placeholder. To use a real LLM, update the logic in `backend/flask_app.py` in the `ask_llm` function.
- The default backend `/ask` endpoint is still expected at port 8000 (FastAPI or Flask, as you prefer).
- For CORS issues, make sure Flask is running with CORS enabled (already set up).

## Troubleshooting

- If you see connection errors, check that both servers are running and the ports match the URLs in the Flutter code.
- For plugin errors on macOS/iOS, ensure CocoaPods is installed (`sudo gem install cocoapods`).
- For dependency issues, run `pip install -r requirements.txt` (backend) or `flutter pub get` (frontend).

---

For further customization or LLM integration, edit `backend/flask_app.py` and update the `/ask_llm` endpoint.

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
