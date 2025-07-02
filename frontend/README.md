# stack_qna_frontend

A Flutter project for Stack Overflow RAG Q&A.

## Features
- Ask programming questions and get answers from Stack Overflow data (local or Hugging Face)
- Displays tags, score, favorite count, and accepted answer badge for each result
- Lets users select the data source (local, Hugging Face, or LLM)
- Side-by-side comparison of answers from different sources

## Getting Started

1. `cd frontend`
2. `flutter pub get`
3. `flutter run` (web, Android, or iOS)

## API
- Connects to the backend `/ask` endpoint
- Expects response fields: `answer`, `sources` (with `tags`, `score`, `favorite_count`, `accepted_answer_id`), `tokens`, `status`

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
