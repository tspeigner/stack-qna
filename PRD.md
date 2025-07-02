# Product Requirements Document (PRD)

## Project: Stack Overflow RAG Q&A App (Gemini Pro + Flutter)

### Overview
A full-stack question-answering application powered by Retrieval-Augmented Generation (RAG) using Stack Overflow data. The system includes a Flask backend for retrieval and answer generation (via Gemini Pro), and a cross-platform Flutter frontend for user interaction.

---

## 0. Implementation Notes & Changelog
- [2025-07-01] Project initialized with secure .gitignore for backend and frontend.
- Backend supports Flask, Gemini Pro, and advanced Hugging Face streaming with ranking.
- Frontend displays tags, score, favorites, and accepted answer badge.
- All secrets and build artifacts are excluded from version control.

---

## 1. Goals
- Provide accurate, context-rich answers to developer questions.
- Use Stack Overflow Q&A pairs as the primary knowledge base.
- Implement RAG using keyword search and Gemini Pro for grounded response generation.
- Deliver a simple, cross-platform interface via Flutter.
- Enable fast iteration, modular design, and extensibility for future deployment.

---

## 2. Features

### 2.1. Data Ingestion
- Load Q&A pairs from a local JSON file (`data/localdata.json`) or via Hugging Face API (`mikex86/stackoverflow-posts`).
- Allow modular loading or reloading of datasets.

### 2.2. Retrieval
- Retrieve the top 3 relevant Q&A pairs using keyword and tag matching.
- Results are ranked by accepted answer, score, and favorite count.
- Return relevant metadata: tags, score, favorite count, accepted answer ID.

### 2.3. LLM Answer Generation
- Use Gemini Pro API to generate answers, injecting retrieved Q&A content into the prompt.
- Return responses in a consistent, structured JSON format.

### 2.4. API
- `POST /ask` endpoint:
  - **Input:**
    ```json
    { "question": "python", "source": "hf" }
    ```
  - **Output:**
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
- Built with Flask and secured using environment variables.
- Graceful error handling and input validation.

### 2.5. Environment Configuration
- Store secrets and keys in a `.env` file:
  - `GEMINI_API_KEY`
- Loaded at runtime using `python-dotenv`.

### 2.6. Frontend: Flutter UI
- A simple mobile/web-compatible Flutter interface for interacting with the backend API.
- **Features:**
  - Material Design with light theming
  - Input field for entering programming-related questions
  - Button to submit the question to the backend
  - Area to display the generated answer, tags, score, favorites, and accepted answer badge
  - Optional loading spinner and error toast
- **Backend Interaction:**
  - Calls `http://<BACKEND_HOST>:8000/ask` via POST
  - Displays response or error state

---

## 3. Data Storage & Comparison
- All Q&A requests and responses can be saved for analytics and future retrieval.
- The frontend provides options for users to select the data source for Q&A (local, Hugging Face, or LLM) and compare results.
- The UI supports side-by-side comparison of answers from different sources, showing tags, score, favorites, and accepted answer.

---

## 4. Technical Requirements

### Backend
- Python 3.11+
- Flask
- Gemini Pro API
- Hugging Face `datasets` library
- `python-dotenv`, `requests`

### Frontend
- Flutter 3.x
- Dart SDK
- `http` package for API calls

---

## 5. Non-Functional Requirements
- Secure API key handling
- Modular backend (LLM-agnostic, storage-agnostic)
- Logging and traceable errors
- Platform-agnostic Flutter UI
- Quick local setup with clear README

---

## 6. Future Enhancements
- Add streaming LLM response in backend + frontend
- Add rich formatting and copy/paste in UI
- Introduce chat history and session persistence
- Deploy to Firebase (Flutter) and Railway (Flask)

---

## 7. Success Metrics
- Accuracy and relevance of LLM answers (evaluated manually or semi-automated)
- Latency from user input to response (goal: <3s)
- API uptime and error rate
- Usability of Flutter UI (user testing feedback)
- Developer adoption or fork/star count (if open sourced)

---

## 8. Stakeholders
- Product Owner
- ML/AI Engineer (LLM + retrieval)
- Frontend Developer (Flutter)
- Backend Engineer
- End users (developers, students, tinkerers)

---

## 9. Appendix

### Example `POST /ask` Request
```json
{
  "question": "python",
  "source": "hf"
}
```

### Example Response
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

### .env File Example
```env
GEMINI_API_KEY=AIzaSy...
```